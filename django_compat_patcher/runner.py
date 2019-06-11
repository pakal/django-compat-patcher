from compat_patcher.runner import PatchingRunner


class DjangoPatchingRunner(PatchingRunner):


    def _get_software_version(self):
        import django
        return django.get_version()


    def patch_software(self, settings=None):
        """For Django, we separate fixers between those who apply before and after django.setup()."""

        relevant_fixers = self._get_sorted_relevant_fixers()

        print("> relevant_fixers", relevant_fixers)
        pre_fixers = [f for f in relevant_fixers if "fixer_delayed" not in f["fixer_tags"]]
        post_fixers = [f for f in relevant_fixers if "fixer_delayed" in f["fixer_tags"]]
        assert len(relevant_fixers) == len(pre_fixers) + len(post_fixers)

        just_applied_fixers = self._apply_selected_fixers(pre_fixers)
        import django
        django.setup()  # Theoretically idempotent (except regarding logging?)
        just_applied_fixers += self._apply_selected_fixers(post_fixers)

        return just_applied_fixers

