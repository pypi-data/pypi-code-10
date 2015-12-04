# Copyright (c) 2014 The Johns Hopkins University/Applied Physics Laboratory
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import os
import time

from kmip.core import attributes
from kmip.core import enums
from kmip.core import misc
from kmip.core import objects
from kmip.core import primitives
from kmip.core import secrets
from kmip.core import server
from kmip.core import utils

from kmip.core.factories.attributes import AttributeFactory
from kmip.core.factories.keys import KeyFactory
from kmip.core.factories.secrets import SecretFactory

from kmip.core.messages import messages
from kmip.core.messages import contents

from kmip.core.messages.payloads.create import CreateResponsePayload
from kmip.core.messages.payloads.get import GetResponsePayload
from kmip.core.messages.payloads.destroy import DestroyResponsePayload
from kmip.core.messages.payloads.register import RegisterResponsePayload
from kmip.core.messages.payloads.locate import LocateResponsePayload

from kmip.services.server.repo.mem_repo import MemRepo

from kmip.services import results


class KMIPImpl(server.KMIP):

    def __init__(self):
        super(KMIPImpl, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.key_factory = KeyFactory()
        self.secret_factory = SecretFactory()
        self.attribute_factory = AttributeFactory()
        self.repo = MemRepo()

    def create(self, object_type, template_attribute, credential=None):
        self.logger.debug('create() called')
        self.logger.debug('object type = %s' % object_type)
        bit_length = 256
        attributes = template_attribute.attributes
        ret_attributes = []
        if object_type.value != enums.ObjectType.SYMMETRIC_KEY:
            self.logger.debug('invalid object type')
            return self._get_invalid_field_result('invalid object type')
        try:
            alg_attr = self._validate_req_field(
                attributes, enums.AttributeType.CRYPTOGRAPHIC_ALGORITHM.value,
                (enums.CryptographicAlgorithm.AES,), 'unsupported algorithm')
            len_attr = self._validate_req_field(
                attributes, enums.AttributeType.CRYPTOGRAPHIC_LENGTH.value,
                (128, 256, 512), 'unsupported key length', False)
            self._validate_req_field(
                attributes,
                enums.AttributeType.CRYPTOGRAPHIC_USAGE_MASK.value, (), '')
        except InvalidFieldException as e:
            self.logger.debug('InvalidFieldException raised')
            return e.result

        crypto_alg = attributes.CryptographicAlgorithm(
            enums.CryptographicAlgorithm(alg_attr.attribute_value.value))

        if len_attr is None:
            self.logger.debug('cryptographic length not supplied')
            attribute_type = enums.AttributeType.CRYPTOGRAPHIC_LENGTH
            length_attribute = self.attribute_factory.\
                create_attribute(attribute_type, bit_length)
            attributes.append(length_attribute)
            ret_attributes.append(length_attribute)
        else:
            bit_length = len_attr.attribute_value.value

        key = self._gen_symmetric_key(bit_length, crypto_alg)
        s_uuid, uuid_attribute = self._save(key, attributes)
        ret_attributes.append(uuid_attribute)
        template_attribute = objects.TemplateAttribute(
            attributes=ret_attributes)
        return results.CreateResult(
            contents.ResultStatus(
                enums.ResultStatus.SUCCESS),
                object_type=object_type,
                uuid=attributes.UniqueIdentifier(s_uuid),
                template_attribute=template_attribute)

    def create_key_pair(self, common_template_attribute,
                        private_key_template_attribute,
                        public_key_template_attribute):
        raise NotImplementedError()

    def register(self, object_type, template_attribute, secret,
                 credential=None):
        self.logger.debug('register() called')
        self.logger.debug('object type = %s' % object_type)
        attributes = template_attribute.attributes
        ret_attributes = []
        if object_type is None:
            self.logger.debug('invalid object type')
            return self._get_missing_field_result('object type')
        if object_type.value != enums.ObjectType.SYMMETRIC_KEY:
            self.logger.debug('invalid object type')
            return self._get_invalid_field_result('invalid object type')
        if secret is None or not isinstance(secret, secrets.SymmetricKey):
            msg = 'object type does not match that of secret'
            self.logger.debug(msg)
            return self._get_invalid_field_result(msg)

        self.logger.debug('Collecting all attributes')
        if attributes is None:
            attributes = []
        attributes.extend(self._get_key_block_attributes(secret.key_block))

        self.logger.debug('Verifying all attributes are valid and set')
        try:
            self._validate_req_field(
                attributes, enums.AttributeType.CRYPTOGRAPHIC_ALGORITHM.value,
                (enums.CryptographicAlgorithm.AES,),
                'unsupported algorithm')
            self._validate_req_field(
                attributes, enums.AttributeType.CRYPTOGRAPHIC_LENGTH.value,
                (128, 256, 512),
                'unsupported key length')
            self._validate_req_field(
                attributes,
                enums.AttributeType.CRYPTOGRAPHIC_USAGE_MASK.value, (), '')
        except InvalidFieldException as e:
            self.logger.debug('InvalidFieldException raised')
            return results.RegisterResult(
                e.result.result_status,
                e.result.result_reason,
                e.result.result_message)

        s_uuid, uuid_attribute = self._save(secret, attributes)
        ret_attributes.append(uuid_attribute)
        template_attribute = objects.TemplateAttribute(
            attributes=ret_attributes)
        return results.RegisterResult(
            contents.ResultStatus(
                enums.ResultStatus.SUCCESS),
                uuid=attributes.UniqueIdentifier(s_uuid),
                template_attribute=template_attribute)

    def rekey_key_pair(self, private_key_unique_identifier,
                       offset, common_template_attribute,
                       private_key_template_attribute,
                       public_key_template_attribute):
        raise NotImplementedError()

    def get(self,
            uuid=None,
            key_format_type=None,
            key_compression_type=None,
            key_wrapping_specification=None,
            credential=None):
        self.logger.debug('get() called')
        ret_value = enums.ResultStatus.OPERATION_FAILED
        if uuid is None or not hasattr(uuid, 'value'):
            self.logger.debug('no uuid provided')
            reason = contents.ResultReason(enums.ResultReason.ITEM_NOT_FOUND)
            message = contents.ResultMessage('')
            return results.GetResult(
                contents.ResultStatus(ret_value), reason, message)
        if key_format_type is None:
            self.logger.debug('key format type is None, setting to raw')
            key_format_type = misc.KeyFormatType(enums.KeyFormatType.RAW)
        if key_format_type.value != enums.KeyFormatType.RAW:
            self.logger.debug('key format type is not raw')
            reason = contents.ResultReason(
                enums.ResultReason.KEY_FORMAT_TYPE_NOT_SUPPORTED)
            message = contents.ResultMessage('')
            return results.GetResult(
                contents.ResultStatus(ret_value), reason, message)
        if key_compression_type is not None:
            self.logger.debug('key compression type is not None')
            reason = contents.ResultReason(
                enums.ResultReason.KEY_COMPRESSION_TYPE_NOT_SUPPORTED)
            message = contents.ResultMessage('')
            return results.GetResult(
                contents.ResultStatus(ret_value), reason, message)
        if key_wrapping_specification is not None:
            self.logger.debug('key wrapping specification is not None')
            reason = contents.ResultReason(
                enums.ResultReason.FEATURE_NOT_SUPPORTED)
            message = contents.ResultMessage(
                'key wrapping is not currently supported')
            return results.GetResult(
                contents.ResultStatus(ret_value), reason, message)

        self.logger.debug('retrieving object from repo')
        managed_object, _ = self.repo.get(uuid.value)

        if managed_object is None:
            self.logger.debug('object not found in repo')
            reason = contents.ResultReason(enums.ResultReason.ITEM_NOT_FOUND)
            message = contents.ResultMessage('')
            return results.GetResult(
                contents.ResultStatus(ret_value), reason, message)

        # currently only symmetric keys are supported, fix this in future
        object_type = attributes.ObjectType(enums.ObjectType.SYMMETRIC_KEY)
        ret_value = enums.ResultStatus.SUCCESS
        return results.GetResult(
            contents.ResultStatus(ret_value), object_type=object_type,
            uuid=uuid, secret=managed_object)

    def destroy(self, uuid):
        self.logger.debug('destroy() called')
        ret_value = enums.ResultStatus.OPERATION_FAILED
        if uuid is None or not hasattr(uuid, 'value'):
            self.logger.debug('no uuid provided')
            reason = contents.ResultReason(enums.ResultReason.ITEM_NOT_FOUND)
            message = contents.ResultMessage('')
            return results.DestroyResult(
                contents.ResultStatus(ret_value), reason, message)

        msg = 'deleting object from repo: {0}'.format(uuid)
        self.logger.debug(msg)
        if not self.repo.delete(uuid.value):
            self.logger.debug('repo did not find and delete managed object')
            reason = contents.ResultReason(enums.ResultReason.ITEM_NOT_FOUND)
            message = contents.ResultMessage('')
            return results.DestroyResult(
                contents.ResultStatus(ret_value), reason, message)

        ret_value = enums.ResultStatus.SUCCESS
        return results.DestroyResult(
            contents.ResultStatus(ret_value), uuid=uuid)

    def locate(self, maximum_items=None, storage_status_mask=None,
               object_group_member=None, attributes=None,
               credential=None):
        self.logger.debug('locate() called')
        msg = 'locating object(s) from repo'
        self.logger.debug(msg)
        try:
            uuids = self.repo.locate(maximum_items, storage_status_mask,
                                     object_group_member, attributes)
            return results.LocateResult(
                contents.ResultStatus(enums.ResultStatus.SUCCESS),
                uuids=uuids)
        except NotImplementedError:
            msg = contents.ResultMessage('Locate Operation Not Supported')
            reason = contents.ResultReason(
                enums.ResultReason.OPERATION_NOT_SUPPORTED)
            return results.LocateResult(
                contents.ResultStatus(enums.ResultStatus.OPERATION_FAILED),
                result_reason=reason, result_message=msg)

    def _validate_req_field(self, attrs, name, expected, msg, required=True):
        self.logger.debug('Validating attribute %s' % name)
        seen = False
        found_attr = None
        for attr in attrs:
            if self._validate_field(attr, name, expected, msg):
                if seen:
                    # TODO check what spec says to do on this
                    msg = 'duplicate attribute: %s' % name
                    self.logger.debug(msg)
                    result = self._get_duplicate_attribute_result(name)
                    raise InvalidFieldException(result)
                seen = True
                found_attr = attr
        if required and not seen:
            result = self._get_missing_field_result(name)
            raise InvalidFieldException(result)
        return found_attr

    def _validate_field(self, attr, name, expected, msg):
        if attr.attribute_name.value == name:
            self.logger.debug('validating attribute %s' % name)
            if not expected or attr.attribute_value.value in expected:
                self.logger.debug('attribute validated')
                return True
            else:
                self.logger.debug('attribute not validated')
                result = self._get_invalid_field_result(msg)
                raise InvalidFieldException(result)
        else:
            return False

    def _get_invalid_field_result(self, msg):
        status = contents.ResultStatus(enums.ResultStatus.OPERATION_FAILED)
        reason = contents.ResultReason(enums.ResultReason.INVALID_FIELD)
        message = contents.ResultMessage(msg)
        return results.OperationResult(status, reason, message)

    def _get_missing_field_result(self, name):
        msg = '%s not supplied' % name
        self.logger.debug(msg)
        status = contents.ResultStatus(enums.ResultStatus.OPERATION_FAILED)
        reason = contents.ResultReason(enums.ResultReason.ITEM_NOT_FOUND)
        message = contents.ResultMessage(msg)
        return results.OperationResult(status, reason, message)

    def _get_duplicate_attribute_result(self, name):
        msg = '%s supplied multiple times' % name
        self.logger.debug(msg)
        status = contents.ResultStatus(enums.ResultStatus.OPERATION_FAILED)
        reason = contents.ResultReason(enums.ResultReason.INDEX_OUT_OF_BOUNDS)
        message = contents.ResultMessage(msg)
        return results.OperationResult(status, reason, message)

    def _gen_symmetric_key(self, bit_length, crypto_alg):
        key_format_type = misc.KeyFormatType(enums.KeyFormatType.RAW)
        key_material = objects.KeyMaterial(os.urandom(int(bit_length/8)))
        key_value = objects.KeyValue(key_material)
        crypto_length = attributes.CryptographicLength(bit_length)
        key_block = objects.KeyBlock(
            key_format_type, None, key_value, crypto_alg, crypto_length, None)
        return secrets.SymmetricKey(key_block)

    def _save(self, key, attributes):
        s_uuid = self.repo.save(key, attributes)
        self.logger.debug('creating object with uuid = %s' % s_uuid)
        attribute_type = enums.AttributeType.UNIQUE_IDENTIFIER
        attribute = self.attribute_factory.create_attribute(attribute_type,
                                                            s_uuid)
        attributes.append(attribute)
        # Calling update to also store the UUID
        self.repo.update(s_uuid, key, attributes)
        return s_uuid, attribute

    def _get_key_block_attributes(self, key_block):
        self.logger.debug('getting all key attributes from key block')
        attributes = []
        if key_block.cryptographic_algorithm is not None:
            self.logger.debug('crypto_alg set on key block')
            self.logger.debug('adding crypto algorithm attribute')
            at = enums.AttributeType.CRYPTOGRAPHIC_ALGORITHM
            alg = key_block.cryptographic_algorithm.value
            attributes.append(self.attribute_factory.create_attribute(at, alg))
        if key_block.cryptographic_length is not None:
            self.logger.debug('crypto_length set on key block')
            self.logger.debug('adding crypto length attribute')
            at = enums.AttributeType.CRYPTOGRAPHIC_LENGTH
            len = key_block.cryptographic_length.value
            attributes.append(self.attribute_factory.create_attribute(at, len))
        self.logger.debug('getting key value attributes')
        if key_block.key_wrapping_data is not None:
            self.logger.debug('no wrapping data so key value is struct')
            kv = key_block.key_value
            if isinstance(kv, objects.KeyValue):
                kv = key_block.key_value
                if kv.attributes is not None:
                    self.logger.debug('adding the key value struct attributes')
                    attributes.extend(kv.attributes)
        return attributes


class InvalidFieldException(Exception):

    def __init__(self, result):
        super(InvalidFieldException, self).__init__()
        self.result = result


class Processor(object):
    def __init__(self, handler):
        self.logger = logging.getLogger(__name__)
        self._handler = handler

    def process(self, istream, ostream):
        stream = istream.read()

        if primitives.Base.is_tag_next(
                enums.Tags.REQUEST_MESSAGE, stream):
            message = messages.RequestMessage()
            message.read(stream)
            try:
                result = self._process_request(message)
            except Exception as e:
                raise e
            tstream = utils.BytearrayStream()
            result.write(tstream)
            ostream.write(tstream.buffer)
        elif primitives.Base.is_tag_next(
                enums.Tags.RESPONSE_MESSAGE, stream):
            message = messages.ResponseMessage()
            message.read(stream)
            self._process_response(message)
        else:
            raise ValueError('Processing error: stream contains unknown '
                             'message type')

    def _process_request(self, message):
        header = message.request_header

        protocol_version = header.protocol_version
#        maximum_response_size = header.maximum_response_size
        asynchronous_indicator = header.asynchronous_indicator
#        authentication = header.authentication
        batch_error_cont_option = header.batch_error_cont_option
#        batch_order_option = header.batch_order_option
#        time_stamp = header.time_stamp
        request_batch_count = header.batch_count.value

        # TODO (peter-hamilton) Log receipt of message with time stamp

        if asynchronous_indicator is None:
            asynchronous_indicator = contents.AsynchronousIndicator(False)

        if batch_error_cont_option is None:
            batch_error_cont_option = contents.BatchErrorContinuationOption(
                enums.BatchErrorContinuationOption.STOP)

        request_batch_items = message.batch_items
        response_batch_items = []

        for i in range(request_batch_count):
            request_batch_item = request_batch_items[i]
            failure_occurred = False

            operation = request_batch_item.operation
            ubi_id = request_batch_item.unique_batch_item_id
            payload = request_batch_item.request_payload
            message_extension = request_batch_item.message_extension

            result = self._process_operation(operation, payload)

            result_status = result[0]
            result_reason = result[1]
            result_message = result[2]
            asyn_cv = None
            response_payload = None
            message_extension = None

            if result_status.value is enums.ResultStatus.SUCCESS:
                response_payload = result[3]
            elif result_status.value is enums.ResultStatus.OPERATION_FAILED:
                failure_occurred = True
                result_reason = result[1]
            elif result_status.value is enums.ResultStatus.OPERATION_PENDING:
                # TODO (peter-hamilton) Need to add a way to track async
                # TODO (peter-hamilton) operations.
                asyn_cv = b'\x00'
            elif result_status.value is enums.ResultStatus.OPERATION_UNDONE:
                result_reason = result[1]
            else:
                msg = 'Unrecognized operation result status: {0}'
                raise RuntimeError(msg.format(result_status))

            resp_bi = messages.ResponseBatchItem(
                operation=operation,
                unique_batch_item_id=ubi_id,
                result_status=result_status,
                result_reason=result_reason,
                result_message=result_message,
                async_correlation_value=asyn_cv,
                response_payload=response_payload,
                message_extension=message_extension)
            response_batch_items.append(resp_bi)

            if failure_occurred:
                if (batch_error_cont_option.value is \
                        enums.BatchErrorContinuationOption.STOP):
                    break
                elif (batch_error_cont_option.value is \
                        enums.BatchErrorContinuationOption.UNDO):
                    # TODO (peter-hamilton) Tell client to undo operations.
                    # TODO (peter-hamilton) Unclear what response should be.
                    break
                elif (batch_error_cont_option.value is \
                        enums.BatchErrorContinuationOption.CONTINUE):
                    continue
                else:
                    msg = 'Unrecognized batch error continuation option: {0}'
                    raise RuntimeError(msg.format(batch_error_cont_option))

        response_batch_count = contents.BatchCount(len(response_batch_items))
        response_time_stamp = contents.TimeStamp(int(time.time()))
        response_header = messages.ResponseHeader(
            protocol_version=protocol_version,
            time_stamp=response_time_stamp,
            batch_count=response_batch_count)

        response_message = messages.ResponseMessage(
            response_header=response_header,
            batch_items=response_batch_items)
        return response_message

    def _process_response(self, message):
        raise NotImplementedError()

    def _process_operation(self, operation, payload):
        op = operation.value

        if op is enums.Operation.CREATE:
            return self._process_create_request(payload)
        elif op is enums.Operation.GET:
            return self._process_get_request(payload)
        elif op is enums.Operation.DESTROY:
            return self._process_destroy_request(payload)
        elif op is enums.Operation.REGISTER:
            return self._process_register_request(payload)
        elif op is enums.Operation.LOCATE:
            return self._process_locate_request(payload)
        else:
            raise NotImplementedError()

    def _process_create_request(self, payload):
        object_type = payload.object_type
        template_attribute = payload.template_attribute
        result = self._handler.create(object_type, template_attribute)

        result_status = result.result_status
        result_reason = result.result_reason
        result_message = result.result_message
        created_type = result.object_type
        uuid = result.uuid
        template_attribute = result.template_attribute

        resp_pl = CreateResponsePayload(object_type=created_type,
                                        unique_identifier=uuid,
                                        template_attribute=template_attribute)

        return (result_status, result_reason, result_message, resp_pl)

    def _process_get_request(self, payload):
        uuid = None
        kft = None
        kct = None

        unique_identifier = payload.unique_identifier
        key_format_type = payload.key_format_type
        key_compression_type = payload.key_compression_type
        key_wrapping_specification = payload.key_wrapping_specification

        if unique_identifier is not None:
            uuid = unique_identifier
        if key_format_type is not None:
            kft = key_format_type
        if key_compression_type is not None:
            kct = key_compression_type

        result = self._handler.get(uuid, kft, kct,
                                   key_wrapping_specification)

        result_status = result.result_status
        result_reason = result.result_reason
        result_message = result.result_message
        retrieved_type = result.object_type
        uuid = result.uuid
        secret = result.secret

        resp_pl = GetResponsePayload(object_type=retrieved_type,
                                     unique_identifier=uuid,
                                     secret=secret)

        return (result_status, result_reason, result_message, resp_pl)

    def _process_destroy_request(self, payload):
        uuid = payload.unique_identifier
        result = self._handler.destroy(uuid)

        result_status = result.result_status
        result_reason = result.result_reason
        result_message = result.result_message
        uuid = result.uuid

        payload = DestroyResponsePayload(unique_identifier=uuid)

        return (result_status, result_reason, result_message, payload)

    def _process_register_request(self, payload):
        object_type = payload.object_type
        template_attribute = payload.template_attribute
        secret = payload.secret
        result = self._handler.register(object_type, template_attribute,
                                        secret)

        result_status = result.result_status
        result_reason = result.result_reason
        result_message = result.result_message
        uuid = result.uuid
        template_attr = result.template_attribute

        resp_pl = RegisterResponsePayload(unique_identifier=uuid,
                                          template_attribute=template_attr)

        return (result_status, result_reason, result_message, resp_pl)

    def _process_locate_request(self, payload):
        max_items = payload.maximum_items
        storage_mask = payload.status_storage_mask
        objgrp_member = payload.object_group_member
        attributes = payload.attributes

        result = self._handler.locate(max_items, storage_mask,
                                      objgrp_member, attributes)

        result_status = result.result_status
        result_reason = result.result_reason
        result_message = result.result_message

        uuids = result.uuids

        resp_pl = LocateResponsePayload(unique_identifiers=uuids)

        return (result_status, result_reason, result_message, resp_pl)
