import re


class Validate:

    error_message_templates = {}
    custom_error_messages = {}

    def validate(self, data, rules, custom_messages=None):

        self.error_message_templates = {
            "confirmed": "%s must have a pair field",
            "email": "%s must be a valid email address",
            "required": "%s must be filled",
            "same": "%s has invalid value for same rule"
        }

        self.custom_error_messages = {}

        errors = {}

        for field_name in rules:

            field_rules = rules[field_name].split('|')
            field_errors = []

            for rule in field_rules:

                if rule.startswith("confirmed"):
                    field_errors.extend(self.__validate_confirmed_fields(data, field_name))

                elif rule == "email":
                    field_errors.extend(self.__validate_email_fields(data, field_name))

                elif rule == "required":
                    field_errors.extend(self.__validate_required_fields(data, field_name))

                elif rule.startswith("same"):
                    field_errors.extend(self.__validate_same_fields(data, field_name, rule))

            if len(field_errors) > 0:
                errors[field_name] = field_errors

        return errors

    def __validate_required_fields(self, data, field_name):
        errs = []
        try:
            if data[field_name] == '':
                errs.append(self.return_field_message(field_name, "required"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name, 'required'))

        return errs

    def __validate_email_fields(self, data, field_name):
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        errs, result = self.match_regular_expression(regex, data[field_name], "website")

        if not result:
            errs.append(self.return_field_message(field_name, "email"))
        return errs

    def __validate_confirmed_fields(self, data, field_name):
        errs = []
        confirmation_field = field_name + "_confirmation"

        try:
            if confirmation_field not in data.keys():
                errs.append(self.return_field_message(field_name, "confirmed"))
            elif self.__validate_same_fields(data, confirmation_field, 'same:' + field_name):
                errs.append(self.return_field_message(field_name, "same"))

        except KeyError:
            errs.append(self.return_no_field_message(field_name, 'confirmed'))
        return errs

    def __validate_same_fields(self, data, field_name, rule):
        ls = rule.split(':')[1].split(',')
        errs = []

        try:
            if data[field_name] != data[ls[0]]:
                errs.append(self.return_field_message(field_name, "same"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name, 'same'))
        return errs

    def match_regular_expression(self, regex, field_name, rule_name):
        comp_re = re.compile(regex, re.IGNORECASE)
        errs = []

        try:
            result = comp_re.match(field_name)
        except KeyError:
            errs.append(self.return_no_field_message(field_name, rule_name))
            result = "error"

        return errs, result

    def return_no_field_message(self, field_name, rule_name):
        if self.custom_error_messages.__contains__(field_name + ".no_field"):
            return self.custom_error_messages[field_name + ".no_field"]
        else:
            return self.error_message_templates['no_field'] % (field_name, rule_name)

    def return_field_message(self, field_name, rule_name):
        if self.custom_error_messages.__contains__(field_name + "." + rule_name):
            return self.custom_error_messages[field_name + "." + rule_name]
        else:
            return self.error_message_templates[rule_name] % field_name

    def check(self, data, rules):
        errors = self.validate(data, rules)

        if len(errors) > 0:
            return {
                'is_valid': False,
                'data': {
                    'errors': errors,
                    'message': 'An error occurred'
                }
            }
        else:
            return {
                'is_valid': True,
                'data': {
                    'errors': {},
                    'message': 'OK'
                }
            }
