from django.utils.functional import curry
from django.db.models.signals import pre_save

try:
  from crm.models import Event
  def log_event(model, frm, to):
    if model.pk and hasattr(model, 'related'):
      company = None
      if model.machine._company_field is not None:
        company = getattr(model, model.machine._company_field, None)
      contact = None
      if model.machine._contact_field is not None:
        contact = getattr(model, model.machine._contact_field, None)
      e = Event(
        company=company,
        person=contact,
        mood=None,
        what='{} changed from {} to {}'.format(model, frm, to)
      )
      e.save()
      e.related.connect(model)

except ImportError:
  def log_event(model, frm, to):
    pass

class MachineError(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)


def statemodel_pre_save(sender, instance, raw, using, update_fields, **kwargs):
  if instance.pk is not None:
    stored_instance = instance.__class__.objects.get(pk=instance.pk)
    from_state = stored_instance.state
  else:
    from_state = instance.machine._initial_state
  state = instance.state
  if state != from_state:
    transition = None
    for t, tt in instance._transitions:
      if 'from' in tt and 'to' in tt:
        if (type(tt['from'])== type([]) and from_state in tt['from']) or tt['from']==from_state or tt['from']=='*':
          if tt['to'] == state:
            transition = getattr(instance, t)
            break
    if transition is None:
      raise MachineError("Cannot transition to %s from %s" % (state, from_state))
    instance.state = from_state
    transition(save=False)


class Machine(object):

  def __init__(self, model, states, **kwargs):
    self.model = model
    self._company_field = getattr(model, '_company_field', None)
    self._contact_field = getattr(model, '_contact_field', None)
    try:
      self._initial_state = kwargs.pop('initial')
    except:
      raise MachineError("Must give an initial state")
    self._set_initial_or_retrieve_state(self._initial_state)
    self.states = []
    for state in states:
      self.states.append(state)
    self.states = tuple(self.states)
    pre_save.connect(statemodel_pre_save, sender=self.model.__class__, dispatch_uid='{}_state_presave'.format(self.model.__class__))


  def _extract_from_state(self, kwargs):
    try:
      coming_from = kwargs.pop('from')
    except KeyError:
      raise MachineError("Missing 'from'; must transtion from a state")

    if isinstance(coming_from, str):
      if coming_from not in self.states and coming_from != '*':
        raise MachineError("from: '%s' is not a registered state" % coming_from)
    elif isinstance(coming_from, list):
      for state in coming_from:
        if state not in self.states:
          raise MachineError("from: '%s' is not a registered state" % coming_from)
    return coming_from

  def _extract_to_state(self, kwargs):
    try:
      going_to = kwargs.pop('to')
    except KeyError:
      raise MachineError("Missing 'to'; must transtion to a state")

    if going_to not in self.states:
      raise MachineError("to: '%s' is not a registered state" % coming_from)
    return going_to

  def _set_initial_or_retrieve_state(self, initial):
    try:
      self.state = self._update_state_from_model()
    except AttributeError:
      raise MachineError("The model for this state machine needs a state field in the database")
    if not self.model.state:
      self.state = self._update_model(initial, False)

  def _update_state_from_model(self):
    self.state = self.model.state

  def _update_model(self, state, save=True):
    self.model.state = state
    if save:
      self.model.save()
    self.state = self.model.state

  def end_state(self, save=True, **kwargs):
    if self.model.pk:
      model = self.model.__class__.objects.get(pk=self.model.pk)
      self.state = model.state
    else:
      self._update_state_from_model()
    from_state = self.state
    state = kwargs.get('state')
    from_states = kwargs.get('from_states')
    from_states = from_states if from_states != "*" else [self.state]
    if self.state in from_states:
      trigger_method = 'state_change_{}'.format(state)
      log = True
      if hasattr(self.model, trigger_method):
        triggered = getattr(self.model, trigger_method)
        log = triggered(self.state, state)
      self._update_model(state, save)
      if log and save:
        log_event(self.model, from_state, state)
      return self.state
    else:
      raise MachineError("Cannot transition to %s from %s" % (state, self.state))

  def is_state(self, state, *args):
    self._update_state_from_model()
    return self.state == state

  def is_state_group(self, states):
    self._update_state_from_model()
    return self.state in states

  def event(self, end_state, transition):
    coming_from = self._extract_from_state(transition)
    going_to = self._extract_to_state(transition)
    is_state = "is_%s" % going_to
    setattr(self.model, end_state, curry(self.end_state, state=going_to, from_states=coming_from))
    setattr(self.model, is_state, curry(self.is_state, going_to))


class StatefulModelMixin(object):

  _initial_state = 'draft'
  _states = ()
  _state_groups = ()
  _transitions = ()

  def __init__(self, *args, **kwargs):
    super(StatefulModelMixin, self).__init__(*args, **kwargs)
    self.machine = Machine(self, self._states, initial=self._initial_state)
    for t, tt in self._transitions:
      self.machine.event(t, tt.copy())
    for g, gg in self._state_groups:
      is_group = 'is_{}'.format(g)
      setattr(self, is_group, curry(self.machine.is_state_group, gg))
