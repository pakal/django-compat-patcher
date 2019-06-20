from __future__ import absolute_import, print_function, unicode_literals

from compat_patcher_core.runner import PatchingRunner


class DjangoPatchingRunner(PatchingRunner):
    def patch_software(self, settings=None):
        """For Django, we separate fixers between those who apply before and after django.setup()."""

        relevant_fixers = self._get_sorted_relevant_fixers()

        # print("> relevant_fixers", relevant_fixers)
        pre_fixers = [
            f for f in relevant_fixers if "fixer_delayed" not in f["fixer_tags"]
        ]
        post_fixers = [f for f in relevant_fixers if "fixer_delayed" in f["fixer_tags"]]
        assert len(relevant_fixers) == len(pre_fixers) + len(post_fixers)

        fixers_just_applied = self._apply_selected_fixers(pre_fixers)
        import django

        django.setup()  # Theoretically idempotent (except regarding logging?)
        fixers_just_applied += self._apply_selected_fixers(post_fixers)

        # Be consistent with origianl signature
        return dict(fixers_just_applied=fixers_just_applied)
