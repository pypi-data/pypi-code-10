"""
User Account
"""

import datetime
from flask import redirect, request, url_for, session, jsonify, abort, make_response
from webportfolio import (WebPortfolio, route, flash_error, flash_success,
                          flash_info, flash_data, get_flashed_data, register_package, init_app,
                          ModelError, ViewError)
from webportfolio.decorators import (nav_menu, login_required, no_login_required,
                                     with_user_roles)
from webportfolio.ext import (mailer, cache, storage, recaptcha, csrf,
                              user_authenticated, user_not_authenticated)

import webportfolio.utils as utils
from flask_login import (LoginManager, login_user, logout_user, current_user,
                         fresh_login_required, UserMixin)


# Primary Roles
PRIMARY_ROLES = [(90, "SUPERADMIN"),  # ALL MIGHTY, RESERVED FOR SYS ADMIN
                 (80, "ADMIN"),  # App/Site admin
                 (70, "MANAGER"),  # Limited access, but can approve EDITOR Data
                 (60, "EDITOR"),  # Rights to write, manage, publish own data
                 (50, "CONTRIBUTOR"),  # Rights to only write and read own data
                 (10, "USER")  # Simple user
                 ]


register_package(__name__)


# ------------------------------------------------------------------------------

# The user_model create a fully built model with social signin
def model(db):

    class UserRole(db.Model):

        name = db.Column(db.String(75), index=True)
        level = db.Column(db.Integer, index=True)

        @classmethod
        def new(cls, name, level):
            name = utils.slugify(name)
            role = cls.get_by_name(name)
            if not role:
                role = cls.create(name=name, level=level)
            return role

        @classmethod
        def get_by_name(cls, name):
            name = utils.slugify(name)
            return cls.all().filter(cls.name == name).first()

        @classmethod
        def get_by_level(cls, level):
            return cls.all().filter(cls.level == level).first()

    class User(UserMixin, db.Model):

        role_id = db.Column(db.Integer, db.ForeignKey(UserRole.id))
        email = db.Column(db.String(75), index=True, unique=True)
        email_confirmed = db.Column(db.Boolean, default=False)
        password_hash = db.Column(db.String(255))
        has_temp_login = db.Column(db.Boolean, default=False)
        temp_login_token = db.Column(db.String(100), index=True)
        temp_login_expiration = db.Column(db.DateTime)
        first_name = db.Column(db.String(255))
        last_name = db.Column(db.String(255))
        date_of_birth = db.Column(db.Date)
        sex = db.Column(db.String(10))   # To get confusion out of the way, Sex refers to natural/biological features.
        profile_image_url = db.Column(db.String(255))
        signup_method = db.Column(db.String(255))
        active = db.Column(db.Boolean, default=True, index=True)
        last_login = db.Column(db.DateTime)
        last_visited = db.Column(db.DateTime)
        role = db.relationship(UserRole)

        # ------ FLASK-LOGIN REQUIRED METHODS ----------------------------------

        @property
        def is_active(self):
            return self.active

        # ---------- END FLASK-LOGIN REQUIREMENTS ------------------------------

        @classmethod
        def get_by_email(cls, email):
            """
            Return a User by email address
            """
            return cls.all().filter(cls.email == email).first()

        @classmethod
        def get_by_temp_login(cls, token):
            """
            Return a User by temp_login_token
            temp_login_token allows a user to login with the token
            and reset the password
            """
            user = cls.all().filter(cls.temp_login_token == token).first()
            if user:
                now = datetime.datetime.now()
                if user.has_temp_login is True \
                        and user.temp_login_expiration > now:
                    return user
                user.clear_temp_login()
            return None

        @classmethod
        def get_by_oauth(cls, provider, provider_user_id):
            """
            Get a user by OAuth
            :param provider:
            :param provider_user_id:
            :return: User
            """
            oauth = UserOauthLogin.get_by_provider(provider=provider,
                                                   provider_user_id=provider_user_id)
            return oauth.user if oauth else None
        
        @classmethod
        def new(cls,
                email,
                password=None,
                first_name=None,
                last_name=None,
                role="USER",
                signup_method="email",
                profile_image_url=None,
                **kwargs):
            """
            Create a new user account
            """
            user = cls.get_by_email(email)
            if user:
                raise ModelError("User exists already")
            user = cls.create(email=email,
                              first_name=first_name,
                              last_name=last_name,
                              signup_method=signup_method,
                              profile_image_url=profile_image_url)
            if password:
                user.set_password(password)
            if role:
                role_ = UserRole.get_by_name(role.upper())
                if role_:
                    user.update(role_id=role_.id)

            return user

        @property
        def full_name(self):
            """
            Return the full name
            :return:
            """
            return "%s %s" % (self.first_name, self.last_name)

        @property
        def name(self):
            """
            Alias to first_name
            :return:
            """
            return self.first_name

        def password_matched(self, password):
            """
            Check if the password matched the hash
            :returns bool:
            """
            return utils.verify_encrypted_string(password, self.password_hash)

        def set_password(self, password, random=False):
            """
            Encrypt the password and save it in the DB
            Return the password passed or the new password if randomed
            """
            if random:
                password = utils.generate_random_string()
            self.update(password_hash=utils.encrypt_string(password))
            return password

        def set_temp_login(self, expiration=60):
            """
            Create temp login.
            It will allow to have change password on account
            :param expiration: in minutes the time for expiration
            """
            expiration = datetime.datetime.now() + datetime.timedelta(minutes=expiration)
            while True:
                token = utils.generate_random_string(32).lower()
                if not User.all().filter(User.temp_login_token == token).first():
                    break
            self.update(has_temp_login=True,
                        temp_login_token=token,
                        temp_login_expiration=expiration)
            return token

        def clear_temp_login(self):
            self.update(has_temp_login=False,
                        temp_login_token=None,
                        temp_login_expiration=None)

        def add_oauth(self, provider, provider_user_id, **kwargs):
            """
            To attach a user account to an OAUTH login
            :param provider: the name of the provider
            :param provider_user_id: the id
            :param kwargs:
            :return: Return UserOauthLogin
            """
            u = UserOauthLogin.get_by_provider(provider=provider,
                                               provider_user_id=provider_user_id)
            if u:
                return u
            return UserOauthLogin.create(user_id=self.id,
                                         provider=provider,
                                         provider_user_id=provider_user_id,
                                         **kwargs)

        def has_any_roles(self, *roles):
            """
            Check if user has any of the roles requested
            :param roles: tuple of roles string
            :return: bool
            """
            roles = map(utils.slugify, list(roles))
            for r in UserRole.all().filter(UserRole.name.in_(roles)):
                if r.id == self.role_id:
                    return True
            return False

    class UserOauthLogin(db.Model):
        user_id = db.Column(db.Integer, db.ForeignKey(User.id))
        provider = db.Column(db.String(50), index=True)
        provider_user_id = db.Column(db.String(255))
        name = db.Column(db.String(255))
        email = db.Column(db.String(255))
        profile_image_url = db.Column(db.String(255))
        access_token = db.Column(db.String(255))
        access_key_id = db.Column(db.String(255))
        access_secret_key = db.Column(db.String(255))
        link = db.Column(db.String(255))
        user = db.relationship(User, backref="oauth_logins")

        @classmethod
        def get_by_provider(cls, provider, provider_user_id):
            """
            Returns the entry of the provider and user id
            :params provider: str - the provider name
            :params provider_user_id: 
            """
            return cls.all()\
                .filter(cls.provider == provider)\
                .filter(cls.provider_user_id == provider_user_id)\
                .first()

    return utils.to_struct(User=User,
                           Role=UserRole,
                           OauthLogin=UserOauthLogin)

# ------------------------------------------------------------------------------

def account(view, **kwargs):
    """
    This view is extendable

    kwargs:
        - on_signin_view
        - on_signout_view
        - template_dir

    """

    view_name = view.__name__
    model = kwargs.pop("model")
    User = model.User.User

    nav_menu_context = dict(module_=view.__module__, class_=view.__name__)

    login_view = "UserAccount:login"
    on_signin_view = kwargs["on_signin_view"] if "on_signin_view" \
                                                 in kwargs else "Index:index"
    on_signout_view = kwargs["on_signout_view"] if "on_signout_view" \
                                                   in kwargs else "Index:index"
    template_dir = kwargs["template_dir"] if "template_dir" \
                                             in kwargs else "WebPortfolio/Package/User/Account"
    template_page = template_dir + "/%s.html"

    login_manager = LoginManager()
    login_manager.login_view = login_view
    login_manager.login_message_category = "error"
    init_app(login_manager.init_app)

    @login_manager.user_loader
    def load_user(userid):
        return User.get(userid)

    class Account(object):
        decorators = view.decorators + [login_required]

        SESSION_KEY_SET_EMAIL_DATA = "set_email_tmp_data"
        TEMP_DATA_KEY = "login_tmp_data"

        @property
        def tmp_data(self):
            return session[self.TEMP_DATA_KEY]

        @tmp_data.setter
        def tmp_data(self, data):
            session[self.TEMP_DATA_KEY] = data

        @classmethod
        def _login_enabled(cls):
            if not cls.config_("MODULE_USER_ACCOUNT_ENABLE_LOGIN"):
                abort(403)

        @classmethod
        def _signup_enabled(cls):
            if not cls.config_("MODULE_USER_ACCOUNT_ENABLE_SIGNUP"):
                abort(403)

        @classmethod
        def login_user(cls, user):
            login_user(user)
            now = datetime.datetime.now()
            user.update(last_login=now, last_visited=now)

        @classmethod
        def _oauth_enabled(cls):
            if not cls.config_("MODULE_USER_ACCOUNT_ENABLE_OAUTH_LOGIN"):
                abort(403)

        @nav_menu("Login",
                  endpoint="UserAccount:login",
                  show=user_not_authenticated, **nav_menu_context)
        @route("login/", methods=["GET", "POST"], endpoint="UserAccount:login")
        @no_login_required
        def login(self):
            """ Login page """

            self._login_enabled()
            logout_user()
            self.tmp_data = None
            self.meta_(title="Login")

            if request.method == "POST":
                email = request.form.get("email").strip()
                password = request.form.get("password").strip()

                if not email or not password:
                    flash_error("Email or Password is empty")
                    return redirect(url_for(login_view, next=request.form.get("next")))

                user = User.get_by_email(email)
                if user and user.password_hash and user.password_matched(password):
                    self.login_user(user)
                    return redirect(request.form.get("next") or url_for(on_signin_view))
                else:
                    flash_error("Email or Password is invalid")
                    return redirect(url_for(login_view, next=request.form.get("next")))

            return self.render_(login_url_next=request.args.get("next", ""),
                               login_url_default=url_for(on_signin_view),
                               signup_enabled=self.config_("MODULE_USER_ACCOUNT_ENABLE_SIGNUP"),
                               oauth_enabled=self.config_("MODULE_USER_ACCOUNT_ENABLE_OAUTH_LOGIN"),
                               view_template_=template_page % "login")

        @nav_menu("Logout",
                  endpoint="UserAccount:logout",
                  show=user_authenticated,
                  order=100, **nav_menu_context)
        @route("logout/", endpoint="UserAccount:logout")
        @no_login_required
        def logout(self):
            logout_user()
            return redirect(url_for(on_signout_view or login_view))

        @nav_menu("Signup",
                  endpoint="UserAccount:signup",
                  show=[user_not_authenticated], **nav_menu_context)
        @route("signup/", methods=["GET", "POST"], endpoint="UserAccount:signup")
        @no_login_required
        def signup(self):
            """
            For Email Signup
            :return:
            """
            self._login_enabled()
            self._signup_enabled()
            self.meta_(title="Signup")

            if request.method == "POST":
                # reCaptcha
                if not recaptcha.verify():
                    flash_error("Invalid Security code")
                    return redirect(url_for("UserAccount:signup",
                                            next=request.form.get("next")))
                try:
                    name = request.form.get("name")
                    email = request.form.get("email")
                    password = request.form.get("password")
                    password2 = request.form.get("password2")
                    profile_image_url = request.form.get("profile_image_url", None)

                    if not name:
                        raise ViewError("Name is required")
                    elif not utils.is_valid_email(email):
                        raise ViewError("Invalid email address '%s'" % email)
                    elif not password.strip() or password.strip() != password2.strip():
                        raise ViewError("Passwords don't match")
                    elif not utils.is_valid_password(password):
                        raise ViewError("Invalid password")
                    else:
                        new_account = User.new(email=email,
                                        password=password.strip(),
                                        first_name=name,
                                        profile_image_url=profile_image_url,
                                        signup_method="email")

                        self.login_user(new_account)
                        return redirect(request.form.get("next") or url_for(on_signin_view))
                except Exception as ex:
                    flash_error(ex.message)
                return redirect(url_for("UserAccount:signup",
                                        next=request.form.get("next")))

            logout_user()
            return self.render_(login_url_next=request.args.get("next", ""),
                               view_template_=template_page % "signup")

        @route("lost-password/",
               methods=["GET", "POST"],
               endpoint="UserAccount:lost_password")
        @no_login_required
        def lost_password(self):
            self._login_enabled()
            logout_user()

            self.meta_(title="Lost Password")

            if request.method == "POST":
                email = request.form.get("email")
                user = User.get_by_email(email)
                if user:
                    delivery = self.config_("MODULE_USER_ACCOUNT_RESET_PASSWORD_METHOD")

                    new_password = None
                    if delivery.upper() == "TOKEN":
                        token = user.set_temp_login()
                        url = url_for("UserAccount:reset_password",
                                      token=token,
                                      _external=True)
                    else:
                        new_password = user.set_password(password=None, random=True)
                        url = url_for("UserAccount:login", _external=True)

                    mailer.send_template("reset-password.txt",
                                         method_=delivery,
                                         to=user.email,
                                         name=user.email,
                                         url=url,
                                         new_password=new_password)

                    flash_success("A new password has been sent to '%s'" % email)
                else:
                    flash_error("Invalid email address")
                return redirect(url_for(login_view))
            else:
                return self.render_(view_template_=template_page % "lost_password")


        @nav_menu("Account Settings",
                  endpoint="UserAccount:account_settings",
                  order=99,
                  show=user_authenticated, **nav_menu_context)
        @route("account-settings",
               methods=["GET", "POST"],
               endpoint="UserAccount:account_settings")
        @fresh_login_required
        def account_settings(self):
            self.meta_(title="Account Settings")

            if request.method == "POST":
                action = request.form.get("action")
                try:
                    action = action.lower()
                    #
                    if action == "info":
                        first_name = request.form.get("first_name").strip()
                        last_name = request.form.get("last_name", "").strip()

                        data = {
                            "first_name": first_name,
                            "last_name": last_name
                        }
                        current_user.update(**data)
                        flash_success("Account info updated successfully!")
                    #
                    elif action == "login":
                        confirm_password = request.form.get("confirm-password").strip()
                        if current_user.password_matched(confirm_password):
                            self.change_login_handler()
                            flash_success("Login Info updated successfully!")
                        else:
                            flash_error("Invalid password")
                    #
                    elif action == "password":
                        confirm_password = request.form.get("confirm-password").strip()
                        if current_user.password_matched(confirm_password):
                            self.change_password_handler()
                            flash_success("Password updated successfully!")
                        else:
                            flash_error("Invalid password")

                    elif action == "profile-photo":
                        file = request.files.get("file")
                        if file:
                            prefix = "profile-photos/%s/" % current_user.id
                            extensions = ["jpg", "jpeg", "png", "gif"]
                            my_photo = storage.upload(file,
                                                      prefix=prefix,
                                                      allowed_extensions=extensions)
                            if my_photo:
                                url = my_photo.url
                                current_user.update(profile_image_url=url)
                                flash_success("Profile Image updated successfully!")
                    else:
                        raise ViewError("Invalid action")

                except Exception as e:
                    flash_error(e.message)

                return redirect(url_for("UserAccount:account_settings"))

            return self.render_(view_template_=template_page % "account_settings")

        @classmethod
        def change_login_handler(cls, user_context=None, email=None):
            if not user_context:
                user_context = current_user
            if not email:
                email = request.form.get("email").strip()

            if not utils.is_valid_email(email):
                raise UserWarning("Invalid email address '%s'" % email)
            else:
                if email != user_context.email and User.get_by_email(email):
                    raise UserWarning("Email exists already '%s'" % email)
                elif email != user_context.email:
                    user_context.update(email=email)
                    return True
            return False

        @classmethod
        def change_password_handler(cls, user_context=None, password=None,
                                    password2=None):
            if not user_context:
                user_context = current_user
            if not password:
                password = request.form.get("password").strip()
            if not password2:
                password2 = request.form.get("password2").strip()

            if password:
                if password != password2:
                    raise UserWarning("Password don't match")
                elif not utils.is_valid_password(password):
                    raise UserWarning("Invalid password")
                else:
                    user_context.set_password(password)
                    return True
            else:
                raise UserWarning("Password is empty")


        # OAUTH Login
        @route("oauth-login/<provider>", methods=["GET", "POST"], endpoint="UserAccount:oauth_login")
        @no_login_required
        def oauth_login(self, provider):
            """ Login via oauth providers """

            self._login_enabled()
            self._oauth_enabled()

            provider = provider.lower()
            result = oauth.login(provider)
            response = oauth.response
            popup_js_custom = {
                "action": "",
                "url": ""
            }

            if result:
                if result.error:
                    pass

                elif result.user:
                    result.user.update()

                    oauth_user = result.user
                    user = User.get_by_oauth(provider=provider,
                                             provider_user_id=oauth_user.id)
                    if not user:
                        if oauth_user.email and User.get_by_email(oauth_user.email):
                            flash_error("Account already exists with this email '%s'. "
                                        "Try to login or retrieve your password " % oauth_user.email)

                            popup_js_custom.update({
                                "action": "redirect",
                                "url": url_for(login_view, next=request.form.get("next"))
                            })

                        else:
                            tmp_data = {
                                "is_oauth": True,
                                "provider": provider,
                                "id": oauth_user.id,
                                "name": oauth_user.name,
                                "picture": oauth_user.picture,
                                "first_name": oauth_user.first_name,
                                "last_name": oauth_user.last_name,
                                "email": oauth_user.email,
                                "link": oauth_user.link
                            }
                            if not oauth_user.email:
                                self.tmp_data = tmp_data

                                popup_js_custom.update({
                                    "action": "redirect",
                                    "url": url_for("UserAccount:setup_login")
                                })

                            else:
                                try:
                                    picture = oauth_user.picture
                                    user = User.new(email=oauth_user.email,
                                                    name=oauth_user.name,
                                                    signup_method=provider,
                                                    profile_image_url=picture
                                                    )
                                    user.add_oauth(provider,
                                                   oauth_user.provider_id,
                                                   name=oauth_user.name,
                                                   email=oauth_user.email,
                                                   profile_image_url=oauth_user.picture,
                                                   link=oauth_user.link)
                                except ModelError as e:
                                    flash_error(e.message)
                                    popup_js_custom.update({
                                        "action": "redirect",
                                        "url": url_for("UserAccount:login")
                                    })
                    if user:
                        self.login_user(user)

                    return self.render_(popup_js=result.popup_js(custom=popup_js_custom),
                                       view_template_=template_page % "oauth_login")
            return response

        @route("setup-login/", methods=["GET", "POST"], endpoint="UserAccount:setup_login")
        def setup_login(self):
            """
            Allows to setup a email password if it's not provided specially
            coming from oauth-login
            :return:
            """
            self._login_enabled()
            self.meta_(title="Setup  Login")

            # Only user without email can set email
            if current_user.is_authenticated() and current_user.email:
                return redirect(url_for("%s:account_settings" % view_name))

            if self.tmp_data:
                if request.method == "POST":
                    if not self.tmp_data["is_oauth"]:
                        return redirect("UserAccount:login")

                    try:
                        email = request.form.get("email")
                        password = request.form.get("password")
                        password2 = request.form.get("password2")

                        if not utils.is_valid_email(email):
                            raise ViewError("Invalid email address '%s'" % email)
                        elif User.get_by_email(email):
                            raise ViewError("An account exists already with this email address '%s' " % email)
                        elif not password.strip() or password.strip() != password2.strip():
                            raise ViewError("Passwords don't match")
                        elif not utils.is_valid_password(password):
                            raise ViewError("Invalid password")
                        else:
                            user = User.new(email=email,
                                            password=password.strip(),
                                            name=self.tmp_data["name"],
                                            profile_image_url=self.tmp_data["picture"],
                                            signup_method=self.tmp_data["provider"])

                            user.add_oauth(self.tmp_data["provider"],
                                           self.tmp_data["id"],
                                           name=self.tmp_data["name"],
                                           email=email,
                                           profile_image_url=self.tmp_data["picture"],
                                           link=self.tmp_data["link"])

                            self.login_user(user)
                            self.tmp_data = None

                        return redirect(request.form.get("next") or url_for(on_signin_view))
                    except Exception as ex:
                        flash_error(ex.message)
                        return redirect(url_for("UserAccount:setup_login"))

                return self.render_(provider=self.tmp_data,
                                   view_template_=template_page % "setup_login")

            else:
                return redirect(url_for("UserAccount:login"))

        @route("reset-password/<token>",
               methods=["GET", "POST"],
               endpoint="UserAccount:reset_password")
        @no_login_required
        def reset_password(self, token):
            self._login_enabled()
            logout_user()

            self.meta_(title="Reset Password")
            user = User.get_by_temp_login(token)
            if user:
                if not user.has_temp_login:
                    return redirect(url_for(on_signin_view))
                if request.method == "POST":
                    try:
                        self.change_password_handler(user_context=user)
                        user.clear_temp_login()
                        flash_success("Password updated successfully!")
                        return redirect(url_for(on_signin_view))
                    except Exception as ex:
                        flash_error("Error: %s" % ex.message)
                        return redirect(url_for("UserAccount:reset_password", token=token))
                else:
                    return self.render_(token=token,
                                       view_template_=template_page % "reset_password")
            else:
                abort(404, "Invalid token")

        @route("oauth-connect", methods=["POST"], endpoint="UserAccount:oauth_connect")
        def oauth_connect(self):
            """ To login via social """
            email = request.form.get("email").strip()
            name = request.form.get("name").strip()
            provider = request.form.get("provider").strip()
            provider_user_id = request.form.get("provider_user_id").strip()
            image_url = request.form.get("image_url").strip()
            next = request.form.get("next", "")
            try:
                current_user.oauth_connect(provider=provider,
                                         provider_user_id=provider_user_id,
                                         email=email,
                                         name=name,
                                         image_url=image_url)
            except Exception as ex:
                flash_error("Unable to link your account")

            return redirect(url_for("%s:account_settings" % view_name))

    return Account


# ------------------------------------------------------------------------------
# ADMIN
PRIVILEDGED_ROLES = ['superadmin', 'admin', 'manager']
def admin(view, **kwargs):
    
    route_base = "user-admin"
    menu_name = "User Admin"

    model = kwargs.get("model")
    User = model.User.User
    Role = model.User.Role

    template_dir = kwargs.get("template_dir", "WebPortfolio/Package/User/Admin")
    template_page = template_dir + "/%s.html"

    # Create a Admin menu for all the methods in Admin
    @nav_menu(menu_name, group="admin")
    class NavMenu(object): pass
    # The nav_menu_context helps attach all the methods to NavMenu
    nav_menu_context = dict(module_=NavMenu.__module__,
                            class_=NavMenu.__name__)
    
    class Admin(object):
        decorators = view.decorators + [login_required, with_user_roles(*PRIVILEDGED_ROLES)]

        @classmethod
        def _validate_admin_roles(cls, user):
            admin = current_user

        @classmethod
        def _user_roles_options(cls):
            _r = Role.all()\
                .filter(Role.level <= current_user.role.level)\
                .order_by(Role.level.desc())
            return [(r.id, r.name) for r in _r]

        @nav_menu("All Users", endpoint="UserAdmin:index", order=1, **nav_menu_context)
        @route("%s/" % route_base, endpoint="UserAdmin:index")
        def user_admin_index(self):

            self.meta_(title="Users - User Admin")
            per_page = self.config_("APPLICATION_PAGINATION_PER_PAGE", 25)

            page = request.args.get("page", 1)
            include_deleted = True if request.args.get("include-deleted") == "y" else False
            name = request.args.get("name")
            email = request.args.get("email")
            role = request.args.get("role")
            sorting = request.args.get("sorting", "first_name__asc")

            users = User.all(include_deleted=include_deleted)
            users = users.join(Role).filter(Role.level <= current_user.role.level)

            if name:
                users = users.filter(User.first_name.contains(name))
            if email:
                users = users.filter(User.email.contains(email))
            if role:
                users = users.filter(User.role_id == int(role))
            if sorting and "__" in sorting:
                col, dir = sorting.split("__", 2)
                if dir == "asc":
                    users = users.order_by(getattr(User, col).asc())
                else:
                    users = users.order_by(getattr(User, col).desc())

            users = users.paginate(page=page, per_page=per_page)

            sorting = [("first_name__asc", "Name ASC"),
                       ("first_name__desc", "Name DESC"),
                       ("email__asc", "Email ASC"),
                       ("email__desc", "Email DESC"),
                       ("created_at__asc", "Signup ASC"),
                       ("created_at__desc", "Signup Desc"),
                       ("last_login__asc", "Login ASC"),
                       ("last_login__desc", "Login Desc")]
            return self.render_(user_roles_options=self._user_roles_options(),
                               sorting_options=sorting,
                               users=users,
                               search_query={
                                   "include-deleted": request.args.get("include-deleted", "n"),
                                   "role": int(request.args.get("role")) if request.args.get("role") else "",
                                   "status": request.args.get("status"),
                                   "first_name": request.args.get("name", ""),
                                   "email": request.args.get("email", ""),
                                   "sorting": request.args.get("sorting")},
                               view_template_=template_page % "index")

        @nav_menu("User Roles", endpoint="UserAdmin:roles", order=2, **nav_menu_context)
        @route("%s/roles" % route_base, methods=["GET", "POST"], endpoint="UserAdmin:roles")
        @with_user_roles("superadmin", "admin")
        def user_admin_roles(self):
            """
            Only admin and super admin can add/remove roles
            RESTRICTED ROLES CAN'T BE CHANGED
            """
            roles_rage_max = 11
            if request.method == "POST":
                try:
                    id = request.form.get("id")
                    name = request.form.get("name")
                    level = request.form.get("level")
                    action = request.form.get("action")

                    if name and level:
                        level = int(level)
                        name = name.upper()
                        _levels = [r[0] for r in Role.PRIMARY]
                        _names = [r[1] for r in Role.PRIMARY]
                        if level in _levels or name in _names:
                            raise ViewError("Can't modify PRIMARY Roles - name: %s, level: %s " % (name, level))
                        else:
                            if id:
                                role = Role.get(id)
                                if role:
                                    if action == "delete":
                                        role.delete()
                                        flash_success("Role '%s' deleted successfully!" % role.name)
                                    elif action == "update":
                                        if role.level != level and Role.get_by_level(level):
                                            raise ViewError("Role Level '%s' exists already" % level)
                                        elif role.name != name and Role.get_by_name(name):
                                            raise ViewError("Role Name '%s'  exists already" % name)
                                        else:
                                            role.update(name=name, level=level)
                                            flash_success("Role '%s (%s)' updated successfully" % (name, level))
                                else:
                                    raise ViewError("Role doesn't exist")
                            else:
                                if Role.get_by_level(level):
                                    raise ViewError("Role Level '%s' exists already" % level)
                                elif Role.get_by_name(name):
                                    raise ViewError("Role Name '%s'  exists already" % name)
                                else:
                                    Role.new(name=name, level=level)
                                    flash_success("New Role '%s (%s)' addedd successfully" % (name, level))
                except Exception as ex:
                    flash_error("Error: %s" % ex.message)
                return redirect(url_for("UserAdmin:roles"))
            else:
                self.meta_(title="User Roles - Users Admin")
                roles = Role.all().order_by(Role.level.desc())

                allocated_levels = [r.level for r in roles]
                levels_options = [(l, l) for l in range(1, roles_rage_max) if l not in allocated_levels]

                return self.render_(roles=roles,
                                   levels_options=levels_options,
                                   view_template_=template_page % "roles")

        @nav_menu("Info", endpoint="UserAdmin:get", show=False, **nav_menu_context)
        @route("%s/<id>" % route_base, endpoint="UserAdmin:get")
        def user_admin_get(self, id):
            self.meta_(title="User Info - Users Admin")
            user = User.get(id, include_deleted=True)
            if not user:
                abort(404, "User doesn't exist")

            if current_user.role.level < user.role.level:
                abort(403, "Not enough rights to access this user info")

            return self.render_(user=user,
                               user_roles_options=self._user_roles_options(),
                               view_template_=template_page % "get")

        @route("%s/post" % route_base, methods=["POST"], endpoint="UserAdmin:post")
        def user_admin_post(self):
            try:
                id = request.form.get("id")
                user = User.get(id, include_deleted=True)
                if not user:
                    flash_error("Can't change user info. Invalid user")
                    return redirect(url_for("UserAdmin:index"))

                if current_user.role.level < user.role.level:
                    abort(403, "Not enough rights to update this user info")

                email = request.form.get("email", "").strip()
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                user_role = request.form.get("user_role")
                action = request.form.get("action")

                if user.id != current_user.id:
                    _role = Role.get(user_role)
                    if not _role:
                        raise ViewError("Invalid role")

                    if current_user.role.name.lower() not in PRIVILEDGED_ROLES:
                        raise ViewError("Not Enough right to change user's info")

                    if action == "activate":
                        user.update(active=True)
                        flash_success("User has been ACTIVATED")
                    elif action == "deactivate":
                        user.update(active=False)
                        flash_success("User is now DEACTIVATED")
                    elif action == "delete":
                        user.delete()
                        flash_success("User has been deleted")
                    elif action == "undelete":
                        user.delete(False)
                        flash_success("User is now active")
                    else:
                        if email and email != user.email:
                            if not utils.is_valid_email(email):
                                raise ViewError("Invalid email address '%s'" % email)
                            else:
                                if User.get_by_email(email):
                                    raise ViewError("Email exists already '%s'" % email)
                                user.update(email=email)

                        user.update(first_name=first_name,
                                    last_name=last_name,
                                    role_id=_role.id)

                else:
                    if email and email != user.email:
                        if not utils.is_valid_email(email):
                            raise ViewError("Invalid email address '%s'" % email)
                        else:
                            if User.get_by_email(email):
                                raise ViewError("Email exists already '%s'" % email)
                            user.update(email=email)
                    user.update(first_name=first_name,
                                last_name=last_name)

                    flash_success("User's Info updated successfully!")
            except Exception as ex:
                flash_error("Error: %s " % ex.message)
            return redirect(url_for("UserAdmin:get", id=id))

        @route("%s/reset-password" % route_base, methods=["POST"], endpoint="UserAdmin:reset_password")
        def user_admin_reset_password(self):
            """
            Reset the password
            :returns string: The new password string
            """
            try:
                id = request.form.get("id")
                user = User.get(id)
                if not user:
                    raise ViewError("Invalid User")

                method_ = self.config_("LOGIN_RESET_PASSWORD_METHOD", "").upper()
                new_password = None
                if method_ == "TOKEN":
                    token = user.set_temp_login()
                    url = url_for("UserAccount:temp_login_token",
                                  token=token,
                                  _external=True)
                else:
                    new_password = user.set_password(password=None, random=True)
                    url = url_for("UserAccount:login", _external=True)

                mailer.send_template("reset-password.txt",
                                     method_=method_,
                                     to=user.email,
                                     name=user.email,
                                     url=url,
                                     new_password=new_password)

                flash_success("Password Reset instruction is sent to email")
            except Exception as ex:
                flash_error("Error: %s " % ex.message)
            return redirect(url_for("UserAdmin:get", id=id))

        @route("%s/create" % route_base, methods=["POST"], endpoint="UserAdmin:create")
        @with_user_roles(*PRIVILEDGED_ROLES)
        def user_admin_create(self):
            try:
                email = request.form.get("email")
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                user_role = request.form.get("user_role")

                _role = Role.get(user_role)
                if not _role:
                    raise ViewError("Invalid role")

                if current_user.role.level < _role.level:
                    raise ViewError("Can't be assigned a greater user role")

                if not first_name:
                    raise ViewError("First Name is required")
                elif not email:
                    raise ViewError("Email is required")
                elif not utils.is_valid_email(email):
                    raise ViewError("Invalid email address")
                if User.get_by_email(email):
                    raise ViewError("Email '%s' exists already" % email)
                else:
                    user = User.new(email=email,
                                    first_name=first_name,
                                    last_name=last_name,
                                    signup_method="email-from-admin",
                                    role_id=_role.id)
                    if user:
                        flash_success("User created successfully!")
                        return redirect(url_for("UserAdmin:get", id=user.id))
                    else:
                        raise ViewError("Couldn't create new user")
            except Exception as ex:
                flash_error("Error: %s" % ex.message)
            return redirect(url_for("UserAdmin:index"))

    return Admin

