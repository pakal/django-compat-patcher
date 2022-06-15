from __future__ import absolute_import, print_function, unicode_literals

# Filters applied first, the special value "*" means "all"
DCP_INCLUDE_FIXER_IDS = "*"
DCP_INCLUDE_FIXER_FAMILIES = []

# Filters applied last
DCP_EXCLUDE_FIXER_IDS = ["fix_behaviour_core_management_parser_optparse",
                         "fix_deletion_contrib_postgres_forms_jsonb_InvalidJSONInput_JSONString",
                         "fix_deletion_contrib_postgres_fields_jsonb_JsonAdapter",
                         "fix_deletion_contrib_postgres_forms_jsonb",
                         "fix_deletion_contrib_postgres_fields_jsonb"]
DCP_EXCLUDE_FIXER_FAMILIES = []

DCP_PATCH_INJECTED_OBJECTS = "__dcp_injected__"

DCP_LOGGING_LEVEL = "INFO"
DCP_ENABLE_WARNINGS = True
