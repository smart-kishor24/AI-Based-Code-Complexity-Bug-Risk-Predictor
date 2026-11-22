"""
Sample Python Code: Deeply nested conditions and anti-patterns.
Contains deep nesting depth, mutable default arguments, and bare except clauses.
"""


def validate_and_parse_records(records, cache=[]):  # Static warning: mutable default
    """
    Parses and verifies data records using deeply nested control flow blocks.
    """
    parsed_results = []
    
    if records is not None:
        if len(records) > 0:
            for item in records:
                if isinstance(item, dict):
                    if "header" in item:
                        header = item["header"]
                        if header.get("valid", False) is True:
                            if "payload" in item:
                                payload = item["payload"]
                                for entry in payload:
                                    if entry.get("active", False):
                                        try:
                                            val = int(entry.get("code", 0))
                                            if val > 100:
                                                if val % 2 == 0:
                                                    parsed_results.append(val)
                                                else:
                                                    parsed_results.append(val * -1)
                                            else:
                                                parsed_results.append(0)
                                        except:  # Static warning: bare except
                                            pass
    return parsed_results
