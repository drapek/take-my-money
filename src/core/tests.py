
class TestMixin:
    def assertDictKeys(self, dict, key_list):
        keys_presence_list = [x in dict for x in key_list]

        if not all(keys_presence_list):
            msg = ""
            msg += f"Following keys can't be found in dict. Keys = "
            for i in range(len(keys_presence_list)):
                if not keys_presence_list[i]:
                    msg += f"{key_list[i]}, "
            raise AssertionError(msg)
