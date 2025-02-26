.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`0.11.13 <https://github.com/ansys/pymechanical/releases/tag/v0.11.13>`_ - 2025-02-07
=====================================================================================

Added
^^^^^

- Add CPython feature flag for `ansys-mechanical`  cli `#1049 <https://github.com/ansys/pymechanical/pull/1049>`_
- Rpyc integration `#1055 <https://github.com/ansys/pymechanical/pull/1055>`_
- Add "what's new" sections to changelog `#1057 <https://github.com/ansys/pymechanical/pull/1057>`_
- Create option for PyPIM to be installed separately `#1060 <https://github.com/ansys/pymechanical/pull/1060>`_


Fixed
^^^^^

- Add explicit interface support `#1058 <https://github.com/ansys/pymechanical/pull/1058>`_
- Disable app poster test `#1072 <https://github.com/ansys/pymechanical/pull/1072>`_


Documentation
^^^^^^^^^^^^^

- Clarify support guidelines `#1061 <https://github.com/ansys/pymechanical/pull/1061>`_


Maintenance
^^^^^^^^^^^

- update CHANGELOG for v0.11.12 `#1050 <https://github.com/ansys/pymechanical/pull/1050>`_
- Bump the doc group with 4 updates `#1054 <https://github.com/ansys/pymechanical/pull/1054>`_
- pre-commit automatic update `#1056 <https://github.com/ansys/pymechanical/pull/1056>`_, `#1067 <https://github.com/ansys/pymechanical/pull/1067>`_, `#1081 <https://github.com/ansys/pymechanical/pull/1081>`_
- Raise error if Ansys has no attribute Mechanical `#1062 <https://github.com/ansys/pymechanical/pull/1062>`_
- Bump grpcio from 1.69.0 to 1.70.0 in the core group `#1063 <https://github.com/ansys/pymechanical/pull/1063>`_
- Bump panel from 1.5.5 to 1.6.0 in the doc group `#1064 <https://github.com/ansys/pymechanical/pull/1064>`_
- Upgrade `ansys-pythonnet` version `#1066 <https://github.com/ansys/pymechanical/pull/1066>`_
- Add gitattributes and renormalize files `#1069 <https://github.com/ansys/pymechanical/pull/1069>`_
- Bump sphinx-notfound-page from 1.0.4 to 1.1.0 in the doc group `#1079 <https://github.com/ansys/pymechanical/pull/1079>`_
- Bump plotly from 5.24.1 to 6.0.0 `#1080 <https://github.com/ansys/pymechanical/pull/1080>`_
- Upgrade `ansys-sphinx-theme` `#1082 <https://github.com/ansys/pymechanical/pull/1082>`_
- update clr loader version `#1083 <https://github.com/ansys/pymechanical/pull/1083>`_


Test
^^^^

- update poster test `#1065 <https://github.com/ansys/pymechanical/pull/1065>`_

`0.11.12 <https://github.com/ansys/pymechanical/releases/tag/v0.11.12>`_ - 2025-01-16
=====================================================================================

Added
^^^^^

- Update enum and globals `#1037 <https://github.com/ansys/pymechanical/pull/1037>`_
- add poster method that raises an exception `#1038 <https://github.com/ansys/pymechanical/pull/1038>`_
- docker and ci/cd change for 25R1 `#1042 <https://github.com/ansys/pymechanical/pull/1042>`_


Maintenance
^^^^^^^^^^^

- update CHANGELOG for v0.11.11 `#1031 <https://github.com/ansys/pymechanical/pull/1031>`_
- Bump the doc group with 2 updates `#1036 <https://github.com/ansys/pymechanical/pull/1036>`_
- pre-commit automatic update `#1039 <https://github.com/ansys/pymechanical/pull/1039>`_
- Bump `ansys-mechanical-stubs` from 0.1.5 to 0.1.6 `#1044 <https://github.com/ansys/pymechanical/pull/1044>`_
- Update default product version to 25R1 `#1045 <https://github.com/ansys/pymechanical/pull/1045>`_
- Bump `ansys-mechanical-env` version from `0.1.8` to  `0.1.9` `#1048 <https://github.com/ansys/pymechanical/pull/1048>`_

`0.11.11 <https://github.com/ansys/pymechanical/releases/tag/v0.11.11>`_ - 2025-01-08
=====================================================================================

Added
^^^^^

- Add tests for transaction `#985 <https://github.com/ansys/pymechanical/pull/985>`_
- Update private app data creation and add tests `#986 <https://github.com/ansys/pymechanical/pull/986>`_
- Update docstring and ``App.save_as()`` `#1001 <https://github.com/ansys/pymechanical/pull/1001>`_
- Update object state for `print_tree()` `#1005 <https://github.com/ansys/pymechanical/pull/1005>`_
- Option to ignore lock file on open `#1007 <https://github.com/ansys/pymechanical/pull/1007>`_
- Add project directory property `#1022 <https://github.com/ansys/pymechanical/pull/1022>`_


Fixed
^^^^^

- Process return code `#1026 <https://github.com/ansys/pymechanical/pull/1026>`_, `#1029 <https://github.com/ansys/pymechanical/pull/1029>`_
- Background App initialization `#1030 <https://github.com/ansys/pymechanical/pull/1030>`_


Miscellaneous
^^^^^^^^^^^^^

- Remove f-string without placeholders and specify exception type. `#1011 <https://github.com/ansys/pymechanical/pull/1011>`_


Documentation
^^^^^^^^^^^^^

- Update docs with new api `#1000 <https://github.com/ansys/pymechanical/pull/1000>`_


Maintenance
^^^^^^^^^^^

- Bump codecov/codecov-action from 4 to 5 `#983 <https://github.com/ansys/pymechanical/pull/983>`_
- update CHANGELOG for v0.11.10 `#984 <https://github.com/ansys/pymechanical/pull/984>`_
- Bump ansys-sphinx-theme[autoapi] from 1.2.1 to 1.2.2 in the doc group `#988 <https://github.com/ansys/pymechanical/pull/988>`_
- Bump grpcio from 1.68.0 to 1.68.1 in the core group `#990 <https://github.com/ansys/pymechanical/pull/990>`_
- Bump pytest from 8.3.3 to 8.3.4 in the tests group `#991 <https://github.com/ansys/pymechanical/pull/991>`_
- Bump the doc group with 2 updates `#992 <https://github.com/ansys/pymechanical/pull/992>`_, `#999 <https://github.com/ansys/pymechanical/pull/999>`_
- pre-commit automatic update `#993 <https://github.com/ansys/pymechanical/pull/993>`_
- Support python 3.13 `#997 <https://github.com/ansys/pymechanical/pull/997>`_
- Bump clr-loader from 0.2.6 to 0.2.7.post0 in the core group `#1003 <https://github.com/ansys/pymechanical/pull/1003>`_
- Bump matplotlib from 3.9.3 to 3.10.0 in the doc group `#1004 <https://github.com/ansys/pymechanical/pull/1004>`_
- Bump the doc group with 3 updates `#1008 <https://github.com/ansys/pymechanical/pull/1008>`_
- Bump psutil from 6.1.0 to 6.1.1 `#1009 <https://github.com/ansys/pymechanical/pull/1009>`_
- Update license headers for 2025 `#1014 <https://github.com/ansys/pymechanical/pull/1014>`_
- Bump ``ansys-mechanical-stubs`` to 0.1.5 and add typehint to DataModel `#1015 <https://github.com/ansys/pymechanical/pull/1015>`_
- Follow pythonic standard for comparison to None. `#1016 <https://github.com/ansys/pymechanical/pull/1016>`_
- Bump grpcio from 1.68.1 to 1.69.0 in the core group `#1020 <https://github.com/ansys/pymechanical/pull/1020>`_
- Bump sphinx-autodoc-typehints from 2.5.0 to 3.0.0 `#1021 <https://github.com/ansys/pymechanical/pull/1021>`_
- Update ngihtly for pre-release version `#1023 <https://github.com/ansys/pymechanical/pull/1023>`_

`0.11.10 <https://github.com/ansys/pymechanical/releases/tag/v0.11.10>`_ - 2024-11-18
=====================================================================================

Added
^^^^^

- Version input type check `#979 <https://github.com/ansys/pymechanical/pull/979>`_
- Adding new method for connecting to Mechanical instance `#980 <https://github.com/ansys/pymechanical/pull/980>`_


Fixed
^^^^^

- Update embedding script tests `#974 <https://github.com/ansys/pymechanical/pull/974>`_


Documentation
^^^^^^^^^^^^^

- add Mechanical API link to Mechanical Scripting page `#972 <https://github.com/ansys/pymechanical/pull/972>`_


Maintenance
^^^^^^^^^^^

- update CHANGELOG for v0.11.9 `#963 <https://github.com/ansys/pymechanical/pull/963>`_
- Modify how job success is verified for CI/CD `#965 <https://github.com/ansys/pymechanical/pull/965>`_
- Bump mikepenz/action-junit-report from 4 to 5 `#966 <https://github.com/ansys/pymechanical/pull/966>`_
- Bump grpcio from 1.67.0 to 1.67.1 in the core group `#967 <https://github.com/ansys/pymechanical/pull/967>`_
- Bump the doc group with 2 updates `#968 <https://github.com/ansys/pymechanical/pull/968>`_, `#982 <https://github.com/ansys/pymechanical/pull/982>`_
- Bump pytest-cov from 5.0.0 to 6.0.0 `#969 <https://github.com/ansys/pymechanical/pull/969>`_
- Update docs build action container `#971 <https://github.com/ansys/pymechanical/pull/971>`_
- pre-commit automatic update `#977 <https://github.com/ansys/pymechanical/pull/977>`_
- Bump grpcio from 1.67.1 to 1.68.0 in the core group `#981 <https://github.com/ansys/pymechanical/pull/981>`_

`0.11.9 <https://github.com/ansys/pymechanical/releases/tag/v0.11.9>`_ - 2024-10-29
===================================================================================

Added
^^^^^

- add `ansys-mechanical-stubs` as a dependency `#948 <https://github.com/ansys/pymechanical/pull/948>`_
- Add overwrite option for `App.save_as()` `#951 <https://github.com/ansys/pymechanical/pull/951>`_
- add typehints to ExtAPI, Tree, and Graphics `#957 <https://github.com/ansys/pymechanical/pull/957>`_


Fixed
^^^^^

- bandit warnings `#950 <https://github.com/ansys/pymechanical/pull/950>`_
- stubs CLI test `#952 <https://github.com/ansys/pymechanical/pull/952>`_


Maintenance
^^^^^^^^^^^

- update CHANGELOG for v0.11.8 `#946 <https://github.com/ansys/pymechanical/pull/946>`_
- code maintenance `#947 <https://github.com/ansys/pymechanical/pull/947>`_, `#949 <https://github.com/ansys/pymechanical/pull/949>`_
- Bump the core group with 2 updates `#953 <https://github.com/ansys/pymechanical/pull/953>`_
- Bump ansys-sphinx-theme[autoapi] from 1.1.4 to 1.1.6 in the doc group `#954 <https://github.com/ansys/pymechanical/pull/954>`_
- Bump psutil from 6.0.0 to 6.1.0 `#955 <https://github.com/ansys/pymechanical/pull/955>`_
- bump `ansys-mechanical-stubs` to v0.1.4 `#956 <https://github.com/ansys/pymechanical/pull/956>`_
- Bump the doc group with 2 updates `#960 <https://github.com/ansys/pymechanical/pull/960>`_
- Bump usd-core from 24.8 to 24.11 `#961 <https://github.com/ansys/pymechanical/pull/961>`_
- pre-commit automatic update `#962 <https://github.com/ansys/pymechanical/pull/962>`_

`0.11.8 <https://github.com/ansys/pymechanical/releases/tag/v0.11.8>`_ - 2024-10-15
===================================================================================

Added
^^^^^

- launch_gui command `#882 <https://github.com/ansys/pymechanical/pull/882>`_
- Add method to execute script from file for embedding `#902 <https://github.com/ansys/pymechanical/pull/902>`_
- add warning for x11 loaded before init on 25.1+ `#909 <https://github.com/ansys/pymechanical/pull/909>`_
- `ansys-mechanical-ideconfig` command `#935 <https://github.com/ansys/pymechanical/pull/935>`_
- Automatically update pre-commit ci PR with prefix `#936 <https://github.com/ansys/pymechanical/pull/936>`_


Fixed
^^^^^

- Update ``execute_script`` method `#894 <https://github.com/ansys/pymechanical/pull/894>`_
- Adapting braking change for upload action `#895 <https://github.com/ansys/pymechanical/pull/895>`_
- Remove Python class reference. `#901 <https://github.com/ansys/pymechanical/pull/901>`_
- documentation links `#911 <https://github.com/ansys/pymechanical/pull/911>`_
- Throw value error for unsupported version of Mechanical `#917 <https://github.com/ansys/pymechanical/pull/917>`_
- Use "lite" CLR host on windows for 251+ `#920 <https://github.com/ansys/pymechanical/pull/920>`_
- update AUTHORS file `#929 <https://github.com/ansys/pymechanical/pull/929>`_
- Warning for multiple version `#942 <https://github.com/ansys/pymechanical/pull/942>`_


Miscellaneous
^^^^^^^^^^^^^

- use embedding clr host in version 251 `#926 <https://github.com/ansys/pymechanical/pull/926>`_


Documentation
^^^^^^^^^^^^^

- remove ``thispagetitle`` metatag `#897 <https://github.com/ansys/pymechanical/pull/897>`_


Maintenance
^^^^^^^^^^^

- Add vulnerability check `#709 <https://github.com/ansys/pymechanical/pull/709>`_
- update CHANGELOG for v0.11.7 `#889 <https://github.com/ansys/pymechanical/pull/889>`_
- Bump grpcio from 1.66.0 to 1.66.1 in the core group `#891 <https://github.com/ansys/pymechanical/pull/891>`_
- Bump the doc group with 2 updates `#892 <https://github.com/ansys/pymechanical/pull/892>`_
- Bump pytest-print from 1.0.0 to 1.0.1 in the tests group `#898 <https://github.com/ansys/pymechanical/pull/898>`_
- Bump the doc group with 4 updates `#899 <https://github.com/ansys/pymechanical/pull/899>`_, `#907 <https://github.com/ansys/pymechanical/pull/907>`_, `#916 <https://github.com/ansys/pymechanical/pull/916>`_
- Drop python 3.9 `#904 <https://github.com/ansys/pymechanical/pull/904>`_
- Bump pytest from 8.3.2 to 8.3.3 in the tests group `#906 <https://github.com/ansys/pymechanical/pull/906>`_
- Remove unnecessary dependencies `#908 <https://github.com/ansys/pymechanical/pull/908>`_
- Bump ansys-mechanical-env from 0.1.7 to 0.1.8 in the core group `#914 <https://github.com/ansys/pymechanical/pull/914>`_
- Bump pytest-print from 1.0.1 to 1.0.2 in the tests group `#915 <https://github.com/ansys/pymechanical/pull/915>`_
- Bump grpcio from 1.66.1 to 1.66.2 in the core group `#922 <https://github.com/ansys/pymechanical/pull/922>`_
- Bump panel from 1.5.0 to 1.5.1 in the doc group `#923 <https://github.com/ansys/pymechanical/pull/923>`_
- Use static search `#927 <https://github.com/ansys/pymechanical/pull/927>`_
- Bump the doc group with 5 updates `#933 <https://github.com/ansys/pymechanical/pull/933>`_, `#943 <https://github.com/ansys/pymechanical/pull/943>`_
- pre-commit autoupdate `#934 <https://github.com/ansys/pymechanical/pull/934>`_
- Code maintenance `#937 <https://github.com/ansys/pymechanical/pull/937>`_
- pre-commit automatic update `#944 <https://github.com/ansys/pymechanical/pull/944>`_

`0.11.7 <https://github.com/ansys/pymechanical/releases/tag/v0.11.7>`_ - 2024-08-29
===================================================================================

Documentation
^^^^^^^^^^^^^

- Fix doc layout `#888 <https://github.com/ansys/pymechanical/pull/888>`_


Maintenance
^^^^^^^^^^^

- update CHANGELOG for v0.11.6 `#887 <https://github.com/ansys/pymechanical/pull/887>`_

`0.11.6 <https://github.com/ansys/pymechanical/releases/tag/v0.11.6>`_ - 2024-08-28
===================================================================================

Documentation
^^^^^^^^^^^^^

- Refactor `#878 <https://github.com/ansys/pymechanical/pull/878>`_
- Minor changes `#885 <https://github.com/ansys/pymechanical/pull/885>`_


Maintenance
^^^^^^^^^^^

- update CHANGELOG for v0.11.5 `#872 <https://github.com/ansys/pymechanical/pull/872>`_
- Bump grpcio from 1.65.4 to 1.65.5 in the core group `#875 <https://github.com/ansys/pymechanical/pull/875>`_
- Bump the doc group with 4 updates `#876 <https://github.com/ansys/pymechanical/pull/876>`_
- Bump grpcio from 1.65.5 to 1.66.0 in the core group `#880 <https://github.com/ansys/pymechanical/pull/880>`_
- Bump ansys-sphinx-theme[autoapi] from 1.0.5 to 1.0.7 in the doc group `#881 <https://github.com/ansys/pymechanical/pull/881>`_
- [pre-commit.ci] pre-commit autoupdate `#884 <https://github.com/ansys/pymechanical/pull/884>`_

`0.11.5 <https://github.com/ansys/pymechanical/releases/tag/v0.11.5>`_ - 2024-08-13
===================================================================================

Added
^^^^^

- FEAT: Update cheat sheet with quarto `#845 <https://github.com/ansys/pymechanical/pull/845>`_
- Feat: add a layer to load into an existing stage `#857 <https://github.com/ansys/pymechanical/pull/857>`_


Fixed
^^^^^

- Refactor usd export `#858 <https://github.com/ansys/pymechanical/pull/858>`_
- FIX: App plot None check `#860 <https://github.com/ansys/pymechanical/pull/860>`_


Documentation
^^^^^^^^^^^^^

- chore: update CHANGELOG for v0.11.4 `#856 <https://github.com/ansys/pymechanical/pull/856>`_
- MAINT: Cheat sheet `#871 <https://github.com/ansys/pymechanical/pull/871>`_

Dependencies
^^^^^^^^^^^^


- MAINT: update ansys-sphinx-theme `#863 <https://github.com/ansys/pymechanical/pull/863>`_
- MAINT: Bump the doc group across 1 directory with 4 updates `#866 <https://github.com/ansys/pymechanical/pull/866>`_
- MAINT: Bump ansys/actions from 6 to 7 `#868 <https://github.com/ansys/pymechanical/pull/868>`_
- MAINT: Bump matplotlib from 3.9.1 to 3.9.1.post1 `#869 <https://github.com/ansys/pymechanical/pull/869>`_
- [pre-commit.ci] pre-commit autoupdate `#870 <https://github.com/ansys/pymechanical/pull/870>`_


`0.11.4 <https://github.com/ansys/pymechanical/releases/tag/v0.11.4>`_ - 2024-08-06
===================================================================================

Added
^^^^^

- DOC: Update known issues and limitations `#829 <https://github.com/ansys/pymechanical/pull/829>`_
- Feat: Add option for generating docs without examples `#830 <https://github.com/ansys/pymechanical/pull/830>`_
- Feat: Integrate ansys visualization tool `#846 <https://github.com/ansys/pymechanical/pull/846>`_


Changed
^^^^^^^

- chore: update CHANGELOG for v0.11.3 `#824 <https://github.com/ansys/pymechanical/pull/824>`_
- Maint: Update new labels `#836 <https://github.com/ansys/pymechanical/pull/836>`_
- MAINT: Update ``shims.material_import`` `#837 <https://github.com/ansys/pymechanical/pull/837>`_
- [pre-commit.ci] pre-commit autoupdate `#844 <https://github.com/ansys/pymechanical/pull/844>`_


Fixed
^^^^^

- Maint: Update qk_07 test `#833 <https://github.com/ansys/pymechanical/pull/833>`_
- Maint: Update qk07 `#848 <https://github.com/ansys/pymechanical/pull/848>`_
- use "OnWorkbenchReady" to update globals `#854 <https://github.com/ansys/pymechanical/pull/854>`_
- fix: underline issue with changelog.rst section generation `#855 <https://github.com/ansys/pymechanical/pull/855>`_


Dependencies
^^^^^^^^^^^^

- MAINT: Bump grpcio from 1.64.1 to 1.65.1 in the core group `#826 <https://github.com/ansys/pymechanical/pull/826>`_
- MAINT: Bump pytest from 8.2.2 to 8.3.1 in the tests group `#827 <https://github.com/ansys/pymechanical/pull/827>`_
- MAINT: Bump the doc group with 4 updates `#828 <https://github.com/ansys/pymechanical/pull/828>`_
- MAINT: Bump pytest from 8.3.1 to 8.3.2 in the tests group `#838 <https://github.com/ansys/pymechanical/pull/838>`_
- MAINT: Bump plotly from 5.22.0 to 5.23.0 in the doc group `#839 <https://github.com/ansys/pymechanical/pull/839>`_
- MAINT: Bump usd-core from 24.3 to 24.8 `#841 <https://github.com/ansys/pymechanical/pull/841>`_
- MAINT: Bump sphinxcontrib-websupport from 1.2.7 to 2.0.0 `#842 <https://github.com/ansys/pymechanical/pull/842>`_


Miscellaneous
^^^^^^^^^^^^^

- DOC: Add documentation for ``launch_mechanical`` `#831 <https://github.com/ansys/pymechanical/pull/831>`_


Documentation
^^^^^^^^^^^^^

- add background app class `#849 <https://github.com/ansys/pymechanical/pull/849>`_
- MAINT: Bump grpcio from 1.65.1 to 1.65.4 in the core group `#850 <https://github.com/ansys/pymechanical/pull/850>`_
- Maint: Update qk5 `#852 <https://github.com/ansys/pymechanical/pull/852>`_
- [pre-commit.ci] pre-commit autoupdate `#853 <https://github.com/ansys/pymechanical/pull/853>`_

`0.11.3 <https://github.com/ansys/pymechanical/releases/tag/v0.11.3>`_ - 2024-07-19
===================================================================================

Changed
^^^^^^^

- MAINT: Updates for 242 `#822 <https://github.com/ansys/pymechanical/pull/822>`_
- chore: update CHANGELOG for v0.11.2 `#823 <https://github.com/ansys/pymechanical/pull/823>`_

`0.11.2 <https://github.com/ansys/pymechanical/releases/tag/v0.11.2>`_ - 2024-07-19
===================================================================================

Added
^^^^^

- FEAT: Add known issues and limitation section `#760 <https://github.com/ansys/pymechanical/pull/760>`_
- FEAT: Add test for building gallery `#787 <https://github.com/ansys/pymechanical/pull/787>`_
- FEAT: Add graphics and globals `#790 <https://github.com/ansys/pymechanical/pull/790>`_
- feat: add --script-args argument to ansys-mechanical `#802 <https://github.com/ansys/pymechanical/pull/802>`_
- FEAT: Update print_tree method `#804 <https://github.com/ansys/pymechanical/pull/804>`_


Changed
^^^^^^^

- chore: update CHANGELOG for v0.11.1 `#786 <https://github.com/ansys/pymechanical/pull/786>`_
- [pre-commit.ci] pre-commit autoupdate `#789 <https://github.com/ansys/pymechanical/pull/789>`_, `#801 <https://github.com/ansys/pymechanical/pull/801>`_, `#819 <https://github.com/ansys/pymechanical/pull/819>`_
- MAINT: Update nightly runs for 251 `#803 <https://github.com/ansys/pymechanical/pull/803>`_
- MAINT: Refactor CICD `#806 <https://github.com/ansys/pymechanical/pull/806>`_
- MAINT: Update for 24R2 `#810 <https://github.com/ansys/pymechanical/pull/810>`_
- MAINT: update for docker files 24R2 `#811 <https://github.com/ansys/pymechanical/pull/811>`_
- Update ACT API Reference Guide link `#815 <https://github.com/ansys/pymechanical/pull/815>`_


Fixed
^^^^^

- Fix sentence in architecture file `#800 <https://github.com/ansys/pymechanical/pull/800>`_


Dependencies
^^^^^^^^^^^^

- MAINT: Bump numpy from 1.26.4 to 2.0.0 `#773 <https://github.com/ansys/pymechanical/pull/773>`_
- MAINT: Bump the doc group with 4 updates `#788 <https://github.com/ansys/pymechanical/pull/788>`_
- MAINT: Bump the doc group with 2 updates `#805 <https://github.com/ansys/pymechanical/pull/805>`_
- MAINT: Update dev version of pymechanical `#814 <https://github.com/ansys/pymechanical/pull/814>`_
- MAINT: Bump sphinx from 7.3.7 to 7.4.4 in the doc group `#818 <https://github.com/ansys/pymechanical/pull/818>`_
- MAINT: Update pymech-env `#821 <https://github.com/ansys/pymechanical/pull/821>`_


Miscellaneous
^^^^^^^^^^^^^

- docs: update architecture.rst `#796 <https://github.com/ansys/pymechanical/pull/796>`_
- fix exception when plotting a model with any line bodies `#812 <https://github.com/ansys/pymechanical/pull/812>`_

`0.11.1 <https://github.com/ansys/pymechanical/releases/tag/v0.11.1>`_ - 2024-06-21
===================================================================================

Added
^^^^^

- FEAT: Add an App method to print project tree for embedding scenario `#779 <https://github.com/ansys/pymechanical/pull/779>`_


Changed
^^^^^^^

- Test specific version `#771 <https://github.com/ansys/pymechanical/pull/771>`_
- chore: update CHANGELOG for v0.11.0 `#777 <https://github.com/ansys/pymechanical/pull/777>`_
- chore: bump add-license-headers version to 0.3.2 `#782 <https://github.com/ansys/pymechanical/pull/782>`_


Fixed
^^^^^

- fix sharing app instances, clarify contract `#784 <https://github.com/ansys/pymechanical/pull/784>`_

`0.11.0 <https://github.com/ansys/pymechanical/releases/tag/v0.11.0>`_ - 2024-06-18
===================================================================================


Added
^^^^^

- feat: raise an exception if port or input script aren't provided in batch mode `#753 <https://github.com/ansys/pymechanical/pull/753>`_
- feat: use changelog.rst instead of CHANGELOG.md for release notes `#757 <https://github.com/ansys/pymechanical/pull/757>`_
- Doc: Add embedding api references `#758 <https://github.com/ansys/pymechanical/pull/758>`_
- feat: implement autoapi `#761 <https://github.com/ansys/pymechanical/pull/761>`_


Changed
^^^^^^^

- chore: update CHANGELOG for v0.10.11 `#749 <https://github.com/ansys/pymechanical/pull/749>`_
- MAINT: Delete the apt-get lists after installing packages `#750 <https://github.com/ansys/pymechanical/pull/750>`_
- [pre-commit.ci] pre-commit autoupdate `#774 <https://github.com/ansys/pymechanical/pull/774>`_


Fixed
^^^^^

- FIX: Modify pre-commit hook `#763 <https://github.com/ansys/pymechanical/pull/763>`_
- fix lifetime issue `#768 <https://github.com/ansys/pymechanical/pull/768>`_
- fix pythonnet issue `#772 <https://github.com/ansys/pymechanical/pull/772>`_
- Fix: Remove disable sec check `#776 <https://github.com/ansys/pymechanical/pull/776>`_


Dependencies
^^^^^^^^^^^^

- MAINT: Bump the doc group with 4 updates `#751 <https://github.com/ansys/pymechanical/pull/751>`_
- [pre-commit.ci] pre-commit autoupdate `#752 <https://github.com/ansys/pymechanical/pull/752>`_
- MAINT: Bump the doc group with 3 updates `#755 <https://github.com/ansys/pymechanical/pull/755>`_
- MAINT: Update files as per pyansys standards `#762 <https://github.com/ansys/pymechanical/pull/762>`_
- MAINT: Bump grpcio from 1.64.0 to 1.64.1 in the core group `#764 <https://github.com/ansys/pymechanical/pull/764>`_
- MAINT: Bump pytest from 8.2.1 to 8.2.2 in the tests group `#765 <https://github.com/ansys/pymechanical/pull/765>`_
- MAINT: Bump the doc group with 2 updates `#766 <https://github.com/ansys/pymechanical/pull/766>`_


Miscellaneous
^^^^^^^^^^^^^

- add method to update globals `#767 <https://github.com/ansys/pymechanical/pull/767>`_

`0.10.11 <https://github.com/ansys/pymechanical/releases/tag/v0.10.11>`__ - 2024-05-23
======================================================================================

Added
^^^^^

-  feat: Add tests for animation exports
   `#729 <https://github.com/ansys/pymechanical/pull/729>`__
-  add feature flags to ansys-mechanical cli
   `#735 <https://github.com/ansys/pymechanical/pull/735>`__
-  feat: Add test for deprecation warning
   `#739 <https://github.com/ansys/pymechanical/pull/739>`__

Changed
^^^^^^^

-  chore: update CHANGELOG for v0.10.10
   `#716 <https://github.com/ansys/pymechanical/pull/716>`__
-  Maint: Display image info
   `#717 <https://github.com/ansys/pymechanical/pull/717>`__
-  [pre-commit.ci] pre-commit autoupdate
   `#726 <https://github.com/ansys/pymechanical/pull/726>`__
-  set mono trace env vars before loading mono
   `#734 <https://github.com/ansys/pymechanical/pull/734>`__

Fixed
^^^^^

-  fix: merging coverage step in ci_cd
   `#720 <https://github.com/ansys/pymechanical/pull/720>`__
-  fix: Publish coverage for remote connect
   `#721 <https://github.com/ansys/pymechanical/pull/721>`__
-  fix: Restrict ``protobuf`` <6
   `#722 <https://github.com/ansys/pymechanical/pull/722>`__
-  Fix: add return for poster
   `#727 <https://github.com/ansys/pymechanical/pull/727>`__
-  fix: cli test are not getting coverage
   `#737 <https://github.com/ansys/pymechanical/pull/737>`__
-  fix: adding mechanical libraries
   `#740 <https://github.com/ansys/pymechanical/pull/740>`__
-  feat: Add more coverage on logging
   `#744 <https://github.com/ansys/pymechanical/pull/744>`__
-  fix: Display image and build info only for scheduled run
   `#746 <https://github.com/ansys/pymechanical/pull/746>`__
-  fix: upload coverage files only for latest stable version on release
   workflow `#748 <https://github.com/ansys/pymechanical/pull/748>`__

Dependencies
^^^^^^^^^^^^

-  MAINT: Bump pytest from 8.1.1 to 8.2.0 in the tests group
   `#724 <https://github.com/ansys/pymechanical/pull/724>`__
-  MAINT: Bump the doc group with 3 updates
   `#725 <https://github.com/ansys/pymechanical/pull/725>`__,
   `#743 <https://github.com/ansys/pymechanical/pull/743>`__
-  MAINT: Bump grpcio from 1.62.2 to 1.63.0 in the core group
   `#731 <https://github.com/ansys/pymechanical/pull/731>`__
-  MAINT: Bump the doc group with 2 updates
   `#732 <https://github.com/ansys/pymechanical/pull/732>`__
-  MAINT: Bump grpcio from 1.63.0 to 1.64.0 in the core group
   `#741 <https://github.com/ansys/pymechanical/pull/741>`__
-  MAINT: Bump pytest from 8.2.0 to 8.2.1 in the tests group
   `#742 <https://github.com/ansys/pymechanical/pull/742>`__

Miscellaneous
^^^^^^^^^^^^^

-  Split pyvista into two methods and remove the stability workaround
   for 242 `#718 <https://github.com/ansys/pymechanical/pull/718>`__
-  Update conf.py
   `#723 <https://github.com/ansys/pymechanical/pull/723>`__
-  catch the mono version warning
   `#733 <https://github.com/ansys/pymechanical/pull/733>`__


`0.10.10 <https://github.com/ansys/pymechanical/releases/tag/v0.10.10>`__ - 2024-04-23
======================================================================================


Added
^^^^^

-  Add embedding_scripts marker
   `#662 <https://github.com/ansys/pymechanical/pull/662>`__
-  FEAT: Group dependabot alerts
   `#666 <https://github.com/ansys/pymechanical/pull/666>`__
-  add windows library loader util
   `#672 <https://github.com/ansys/pymechanical/pull/672>`__
-  Feat: Add reports for remote connect tests
   `#690 <https://github.com/ansys/pymechanical/pull/690>`__
-  Feat: Add link check
   `#693 <https://github.com/ansys/pymechanical/pull/693>`__
-  Feat: Add app libraries test
   `#696 <https://github.com/ansys/pymechanical/pull/696>`__
-  Feat: Update ``get_mechanical_path``
   `#707 <https://github.com/ansys/pymechanical/pull/707>`__
-  Feat: ``mechanical-env`` check before running embedding
   `#708 <https://github.com/ansys/pymechanical/pull/708>`__
-  feat: set up doc-deploy-changelog action
   `#710 <https://github.com/ansys/pymechanical/pull/710>`__


Changed
^^^^^^^

-  Doc: fix docs and vale warning
   `#656 <https://github.com/ansys/pymechanical/pull/656>`__
-  Maint: post release change log update 10.9
   `#665 <https://github.com/ansys/pymechanical/pull/665>`__
-  Maint: Auto approve and merge dependabot PR
   `#674 <https://github.com/ansys/pymechanical/pull/674>`__
-  [pre-commit.ci] pre-commit autoupdate
   `#691 <https://github.com/ansys/pymechanical/pull/691>`__,
   `#706 <https://github.com/ansys/pymechanical/pull/706>`__
-  Maint: Add code cov report
   `#692 <https://github.com/ansys/pymechanical/pull/692>`__
-  Maint: Modify nightly run
   `#712 <https://github.com/ansys/pymechanical/pull/712>`__


Fixed
^^^^^

-  Fix: Assign ci bot for dependabot PR
   `#677 <https://github.com/ansys/pymechanical/pull/677>`__
-  Fix: Add matrix python in embedding test
   `#681 <https://github.com/ansys/pymechanical/pull/681>`__
-  Fix: Remove warning message test for remote session launch
   `#682 <https://github.com/ansys/pymechanical/pull/682>`__
-  fix transformation matrix
   `#683 <https://github.com/ansys/pymechanical/pull/683>`__
-  Fix: Modify retrieving path of Mechanical in tests
   `#688 <https://github.com/ansys/pymechanical/pull/688>`__
-  work around instability in 2024R1
   `#695 <https://github.com/ansys/pymechanical/pull/695>`__


Dependencies
^^^^^^^^^^^^

-  MAINT: Bump the doc group with 2 updates
   `#668 <https://github.com/ansys/pymechanical/pull/668>`__,
   `#673 <https://github.com/ansys/pymechanical/pull/673>`__
-  MAINT: Bump the doc group with 1 update
   `#678 <https://github.com/ansys/pymechanical/pull/678>`__
-  first version of 3d visualization with pyvista
   `#680 <https://github.com/ansys/pymechanical/pull/680>`__
-  MAINT: Bump the doc group with 3 updates
   `#689 <https://github.com/ansys/pymechanical/pull/689>`__
-  add open-usd exporter
   `#701 <https://github.com/ansys/pymechanical/pull/701>`__
-  MAINT: Bump the doc group with 5 updates
   `#705 <https://github.com/ansys/pymechanical/pull/705>`__,
   `#715 <https://github.com/ansys/pymechanical/pull/715>`__
-  MAINT: Bump grpcio from 1.62.1 to 1.62.2 in the core group
   `#713 <https://github.com/ansys/pymechanical/pull/713>`__
-  MAINT: Bump ansys/actions from 5 to 6
   `#714 <https://github.com/ansys/pymechanical/pull/714>`__


Miscellaneous
^^^^^^^^^^^^^

-  cleanup `#702 <https://github.com/ansys/pymechanical/pull/702>`__
-  update graphics based on backend changes
   `#711 <https://github.com/ansys/pymechanical/pull/711>`__


`0.10.9 <https://github.com/ansys/pymechanical/releases/tag/v0.10.9>`__ - 2024-03-27
====================================================================================


Added
^^^^^

-  Block 32 bit python for embedding
   `#647 <https://github.com/ansys/pymechanical/pull/647>`__
-  Add usage of cli under embedding
   `#650 <https://github.com/ansys/pymechanical/pull/650>`__
-  Add changelog action
   `#653 <https://github.com/ansys/pymechanical/pull/653>`__


Fixed
^^^^^

-  Fixed make pdf action in doc build
   `#652 <https://github.com/ansys/pymechanical/pull/652>`__
-  Use \_run for better i/o in tests
   `#655 <https://github.com/ansys/pymechanical/pull/655>`__
-  Fix pdf action
   `#664 <https://github.com/ansys/pymechanical/pull/664>`__


Dependencies
^^^^^^^^^^^^

-  Bump ``pytest-cov`` from 4.1.0 to 5.0.0
   `#657 <https://github.com/ansys/pymechanical/pull/657>`__
-  Bump ``ansys-mechanical-env`` from 0.1.4 to 0.1.5
   `#658 <https://github.com/ansys/pymechanical/pull/658>`__


Miscellaneous
^^^^^^^^^^^^^

-  DOC: Improve documentation for the embedded instances.
   `#663 <https://github.com/ansys/pymechanical/pull/663>`__

`0.10.8 <https://github.com/ansys/pymechanical/releases/tag/v0.10.8>`__ -  2024-03-18
=====================================================================================


Added
^^^^^

-  Add poster
   (`#642 <https://github.com/ansys/pymechanical/pull/642>`__)
-  Add LS Dyna unit test
   (`#584 <https://github.com/ansys/pymechanical/pull/584>`__)


Fixed
^^^^^

-  Add logo for dark theme
   (`#601 <https://github.com/ansys/pymechanical/pull/601>`__)
-  Architecture doc
   (`#612 <https://github.com/ansys/pymechanical/pull/612>`__)
-  Put remote example before embedding example
   (`#621 <https://github.com/ansys/pymechanical/pull/621>`__)
-  Minor updates to Architecture doc
   (`#618 <https://github.com/ansys/pymechanical/pull/618>`__)
-  Add MechanicalEnums
   (`#626 <https://github.com/ansys/pymechanical/pull/626>`__)
-  Update Release action to use Stable version of Mechanical
   (`#628 <https://github.com/ansys/pymechanical/pull/628>`__)
-  Update nightly run image version
   (`#636 <https://github.com/ansys/pymechanical/pull/636>`__)
-  Update logo without slash
   (`#640 <https://github.com/ansys/pymechanical/pull/640>`__)


Changed
^^^^^^^

-  Update ``pre-commit``
   (`#610 <https://github.com/ansys/pymechanical/pull/610>`__)
-  Update vale version to 3.1.0
   (`#613 <https://github.com/ansys/pymechanical/pull/613>`__)
-  Update timeout for actions
   (`#631 <https://github.com/ansys/pymechanical/pull/631>`__)
-  Update cheat sheet with ansys-sphinx-theme
   (`#638 <https://github.com/ansys/pymechanical/pull/638>`__)


Dependencies
^^^^^^^^^^^^

-  Bump ``ansys-sphinx-theme`` from 0.13.4 to 0.14.0
   (`#608 <https://github.com/ansys/pymechanical/pull/608>`__)
-  Bump ``plotly`` from 5.18.0 to 5.20.0
   (`#605 <https://github.com/ansys/pymechanical/pull/605>`__,
   `#644 <https://github.com/ansys/pymechanical/pull/644>`__)
-  Bump ``pypandoc`` from 1.12 to 1.13
   (`#609 <https://github.com/ansys/pymechanical/pull/609>`__)
-  Bump ``pytest`` from 8.0.0 to 8.1.1
   (`#606 <https://github.com/ansys/pymechanical/pull/606>`__,
   `#623 <https://github.com/ansys/pymechanical/pull/623>`__,
   `#634 <https://github.com/ansys/pymechanical/pull/634>`__)
-  Bump ``grpcio`` from 1.60.1 to 1.62.1
   (`#620 <https://github.com/ansys/pymechanical/pull/620>`__,
   `#635 <https://github.com/ansys/pymechanical/pull/635>`__)
-  Bump ``pandas`` from 2.2.0 to 2.2.1
   (`#619 <https://github.com/ansys/pymechanical/pull/619>`__)
-  Bump ``matplotlib`` from 3.8.2 to 3.8.3
   (`#607 <https://github.com/ansys/pymechanical/pull/607>`__)
-  Bump ``ansys-mechanical-env`` from 0.1.3 to 0.1.4
   (`#624 <https://github.com/ansys/pymechanical/pull/624>`__)
-  Bump ``pyvista`` from 0.43.3 to 0.43.4
   (`#643 <https://github.com/ansys/pymechanical/pull/643>`__)

`0.10.7 <https://github.com/ansys/pymechanical/releases/tag/v0.10.7>`__ - 2024-02-13
====================================================================================


Added
^^^^^

-  Upload 241 docker files
   (`#567 <https://github.com/ansys/pymechanical/pull/567>`__)
-  Add pre-commit hooks
   (`#575 <https://github.com/ansys/pymechanical/pull/575>`__)
-  Add Automatic version update for Mechanical scripting external links
   (`#585 <https://github.com/ansys/pymechanical/pull/585>`__)
-  Add PyMechanical logo
   (`#592 <https://github.com/ansys/pymechanical/pull/592>`__)


Changed
^^^^^^^

-  Update getting started page
   (`#561 <https://github.com/ansys/pymechanical/pull/561>`__)
-  Update 232 to 241 in docs, docstrings, examples, and tests
   (`#566 <https://github.com/ansys/pymechanical/pull/566>`__)
-  Update workflow versions to run 241 and 242
   (`#590 <https://github.com/ansys/pymechanical/pull/590>`__)


Dependencies
^^^^^^^^^^^^

-  Bump ``pyvista`` from 0.43.1 to 0.43.3
   (`#564 <https://github.com/ansys/pymechanical/pull/564>`__,
   `#598 <https://github.com/ansys/pymechanical/pull/598>`__)
-  Bump ``sphinxcontrib-websupport`` from 1.2.6 to 1.2.7
   (`#562 <https://github.com/ansys/pymechanical/pull/562>`__)
-  Bump ``ansys-sphinx-theme`` from 0.13.0 to 0.13.4
   (`#563 <https://github.com/ansys/pymechanical/pull/563>`__,
   `#586 <https://github.com/ansys/pymechanical/pull/586>`__,
   `#596 <https://github.com/ansys/pymechanical/pull/596>`__)
-  Bump ``pandas`` from 2.1.4 to 2.2.0
   (`#571 <https://github.com/ansys/pymechanical/pull/571>`__)
-  Bump ``sphinxemoji`` from 0.2.0 to 0.3.1
   (`#569 <https://github.com/ansys/pymechanical/pull/569>`__)
-  Bump ``tj-actions/changed-files`` from 41 to 42
   (`#572 <https://github.com/ansys/pymechanical/pull/572>`__)
-  Bump ``panel`` from 1.3.6 to 1.3.8
   (`#570 <https://github.com/ansys/pymechanical/pull/570>`__,
   `#579 <https://github.com/ansys/pymechanical/pull/579>`__)
-  Bump ``peter-evans/create-or-update-comment`` from 3 to 4
   (`#576 <https://github.com/ansys/pymechanical/pull/576>`__)
-  Bump ``pytest`` from 7.4.4 to 8.0.0
   (`#577 <https://github.com/ansys/pymechanical/pull/577>`__)
-  Bump ``sphinx-autodoc-typehints`` from 1.25.2 to 2.0.0
   (`#578 <https://github.com/ansys/pymechanical/pull/578>`__,
   `#597 <https://github.com/ansys/pymechanical/pull/597>`__)
-  Update ``pre-commit``
   (`#580 <https://github.com/ansys/pymechanical/pull/580>`__,
   `#599 <https://github.com/ansys/pymechanical/pull/599>`__)
-  Bump ``ansys.mechanical.env`` from 0.1.2 to 0.1.3
   (`#583 <https://github.com/ansys/pymechanical/pull/583>`__)
-  Bump ``sphinx-autobuild`` from 2021.3.14 to 2024.2.4
   (`#588 <https://github.com/ansys/pymechanical/pull/588>`__)
-  Bump ``pytest-sphinx`` from 0.5.0 to 0.6.0
   (`#587 <https://github.com/ansys/pymechanical/pull/587>`__)
-  Bump ``grpcio`` from 1.60.0 to 1.60.1
   (`#589 <https://github.com/ansys/pymechanical/pull/589>`__)
-  Bump ``numpy`` from 1.26.3 to 1.26.4
   (`#595 <https://github.com/ansys/pymechanical/pull/595>`__)
-  Bump ``imageio`` from 2.33.1 to 2.34.0
   (`#594 <https://github.com/ansys/pymechanical/pull/594>`__)
-  Bump ``mikepenz/action-junit-report`` from 3 to 4
   (`#593 <https://github.com/ansys/pymechanical/pull/593>`__)

`0.10.6 <https://github.com/ansys/pymechanical/releases/tag/v0.10.6>`__ - 2024-01-11
====================================================================================


Added
^^^^^

-  Add release note configuration
   (`#512 <https://github.com/ansys/pymechanical/pull/512>`__)
-  Add 242 to scheduled nightly run
   (`#519 <https://github.com/ansys/pymechanical/pull/519>`__)
-  Add transaction for embedding
   (`#542 <https://github.com/ansys/pymechanical/pull/542>`__)


Fixed
^^^^^

-  Fix pymeilisearch name typo and favicon
   (`#538 <https://github.com/ansys/pymechanical/pull/538>`__)
-  Update the gif to reduce the whitespace
   (`#540 <https://github.com/ansys/pymechanical/pull/540>`__)
-  Update ansys/actions to v5
   (`#541 <https://github.com/ansys/pymechanical/pull/541>`__)
-  Fix cli find mechanical
   (`#550 <https://github.com/ansys/pymechanical/pull/550>`__)


Changed
^^^^^^^

-  Update LICENSE
   (`#548 <https://github.com/ansys/pymechanical/pull/548>`__)
-  Update license headers and package versions
   (`#556 <https://github.com/ansys/pymechanical/pull/556>`__)


Dependencies
^^^^^^^^^^^^

-  Bump ``github/codeql-action`` from 2 to 3
   (`#532 <https://github.com/ansys/pymechanical/pull/532>`__)
-  Update ``pre-commit``
   (`#537 <https://github.com/ansys/pymechanical/pull/537>`__,
   `#545 <https://github.com/ansys/pymechanical/pull/545>`__,
   `#553 <https://github.com/ansys/pymechanical/pull/553>`__)
-  Bump ``pyvista`` from 0.43.0 to 0.43.1
   (`#536 <https://github.com/ansys/pymechanical/pull/536>`__)
-  Bump ``panel`` from 1.3.4 to 1.3.6
   (`#535 <https://github.com/ansys/pymechanical/pull/535>`__,
   `#543 <https://github.com/ansys/pymechanical/pull/543>`__)
-  Bump ``actions/upload-artifact`` and
   ``actions/dwonload-artifact``\ from 3 to 4
   (`#533 <https://github.com/ansys/pymechanical/pull/533>`__)
-  Bump ``jupyter-sphinx`` from 0.4.0 to 0.5.3
   (`#547 <https://github.com/ansys/pymechanical/pull/547>`__)
-  Bump ``tj-actions/changed-files`` from 40 to 41
   (`#544 <https://github.com/ansys/pymechanical/pull/544>`__)
-  Bump ``pytest`` from 7.4.3 to 7.4.4
   (`#546 <https://github.com/ansys/pymechanical/pull/546>`__)
-  Bump ``add-license-headers`` from 0.2.2 to 0.2.4
   (`#549 <https://github.com/ansys/pymechanical/pull/549>`__)
-  Bump ``numpy`` from 1.26.2 to 1.26.3
   (`#551 <https://github.com/ansys/pymechanical/pull/551>`__)

`0.10.5 <https://github.com/ansys/pymechanical/releases/tag/v0.10.5>`__ - 2023-12-15
====================================================================================

Added
^^^^^

-  Add codeql.yml for security checks
   (`#423 <https://github.com/ansys/pymechanical/pull/423>`__)
-  add readonly flag and assertion
   (`#441 <https://github.com/ansys/pymechanical/pull/441>`__)
-  Add PyMeilisearch in documentation
   (`#508 <https://github.com/ansys/pymechanical/pull/508>`__)
-  Add cheetsheat and improve example visibility
   (`#506 <https://github.com/ansys/pymechanical/pull/506>`__)
-  Add mechanical-env to workflow
   (`#521 <https://github.com/ansys/pymechanical/pull/521>`__)
-  Add doc pdf build to workflow
   (`#529 <https://github.com/ansys/pymechanical/pull/529>`__)


Fixed
^^^^^

-  Fix enum printout
   (`#421 <https://github.com/ansys/pymechanical/pull/421>`__)
-  fix appdata tests
   (`#425 <https://github.com/ansys/pymechanical/pull/425>`__)
-  Run all embedding tests & fix appdata tests
   (`#433 <https://github.com/ansys/pymechanical/pull/433>`__)
-  unset all logging environment variables
   (`#434 <https://github.com/ansys/pymechanical/pull/434>`__)
-  pytest –ansys-version dependent on existing install
   (`#439 <https://github.com/ansys/pymechanical/pull/439>`__)
-  Fix app.save method for saving already saved project in current
   session (`#453 <https://github.com/ansys/pymechanical/pull/453>`__)
-  Flexible version for embedding & remote example
   (`#459 <https://github.com/ansys/pymechanical/pull/459>`__)
-  Fix obsolete API call in embedding test
   (`#456 <https://github.com/ansys/pymechanical/pull/456>`__)
-  Fix ignored env passing to cli
   (`#465 <https://github.com/ansys/pymechanical/pull/465>`__
-  Fix private appdata environment variables and folder layout
   (`#474 <https://github.com/ansys/pymechanical/pull/474>`__)
-  Fix hanging embedding tests
   (`#498 <https://github.com/ansys/pymechanical/pull/498>`__)
-  Fix ansys-mechanical finding path
   (`#516 <https://github.com/ansys/pymechanical/pull/516>`__)


Changed
^^^^^^^

-  Update ``pre-commit``
   (`#528 <https://github.com/ansys/pymechanical/pull/528>`__)
-  Update python minimum requirement from 3.8 to 3.9
   (`#484 <https://github.com/ansys/pymechanical/pull/484>`__)
-  remove version limit for protobuf
   (`#432 <https://github.com/ansys/pymechanical/pull/432>`__)
-  remove legacy configuration test
   (`#436 <https://github.com/ansys/pymechanical/pull/436>`__)
-  Update examples page
   (`#450 <https://github.com/ansys/pymechanical/pull/450>`__)
-  remove unneeded try/except
   (`#457 <https://github.com/ansys/pymechanical/pull/457>`__)
-  Updated wording for revn-variations section
   (`#458 <https://github.com/ansys/pymechanical/pull/458>`__)
-  Update temporary file creation in test_app
   (`#466 <https://github.com/ansys/pymechanical/pull/466>`__)
-  Remove .reuse and LICENSES directories & bump add-license-header
   version (`#496 <https://github.com/ansys/pymechanical/pull/496>`__)
-  Replace workbench_lite with mechanical-env in the docs
   (`#522 <https://github.com/ansys/pymechanical/pull/522>`__)


Dependencies
^^^^^^^^^^^^

-  Update ``pre-commit``
   (`#431 <https://github.com/ansys/pymechanical/pull/431>`__,
   `#471 <https://github.com/ansys/pymechanical/pull/471>`__,
   `#489 <https://github.com/ansys/pymechanical/pull/489>`__)
-  Bump ``numpydoc`` from 1.5.0 to 1.6.0
   (`#428 <https://github.com/ansys/pymechanical/pull/428>`__)
-  Bump ``ansys-sphinx-theme`` from 0.11.2 to 0.12.5
   (`#427 <https://github.com/ansys/pymechanical/pull/427>`__,
   `#463 <https://github.com/ansys/pymechanical/pull/463>`__,
   `#480 <https://github.com/ansys/pymechanical/pull/480>`__,
   `#493 <https://github.com/ansys/pymechanical/pull/493>`__)
-  Bump ``grpcio`` from 1.58.0 to 1.60.0
   (`#429 <https://github.com/ansys/pymechanical/pull/429>`__,
   `#485 <https://github.com/ansys/pymechanical/pull/485>`__,
   `#504 <https://github.com/ansys/pymechanical/pull/504>`__,
   `#527 <https://github.com/ansys/pymechanical/pull/527>`__)
-  Bump ``actions/checkout`` from 3 to 4
   (`#426 <https://github.com/ansys/pymechanical/pull/426>`__)
-  Bump ``pyvista`` from 0.42.2 to 0.43.0
   (`#446 <https://github.com/ansys/pymechanical/pull/446>`__,
   `#526 <https://github.com/ansys/pymechanical/pull/526>`__)
-  Bump ``ansys-sphinx-theme`` from 0.12.1 to 0.12.2
   (`#447 <https://github.com/ansys/pymechanical/pull/447>`__)
-  Bump ``stefanzweifel/git-auto-commit-action`` from 4 to 5
   (`#448 <https://github.com/ansys/pymechanical/pull/448>`__)
-  Bump ``numpy`` from 1.26.0 to 1.26.2
   (`#464 <https://github.com/ansys/pymechanical/pull/464>`__,
   `#495 <https://github.com/ansys/pymechanical/pull/495>`__)
-  Bump ``pypandoc`` from 1.11 to 1.12
   (`#470 <https://github.com/ansys/pymechanical/pull/470>`__)
-  Bump ``imageio`` from 2.31.5 to 2.33.1
   (`#469 <https://github.com/ansys/pymechanical/pull/469>`__,
   `#487 <https://github.com/ansys/pymechanical/pull/487>`__,
   `#503 <https://github.com/ansys/pymechanical/pull/503>`__,
   `#524 <https://github.com/ansys/pymechanical/pull/524>`__)
-  Bump ``add-license-headers`` from v0.1.3 to v0.2.0
   (`#472 <https://github.com/ansys/pymechanical/pull/472>`__)
-  Bump ``panel`` from 1.2.3 to 1.3.4
   (`#479 <https://github.com/ansys/pymechanical/pull/479>`__,
   `#486 <https://github.com/ansys/pymechanical/pull/486>`__,
   `#510 <https://github.com/ansys/pymechanical/pull/510>`__,
   `#518 <https://github.com/ansys/pymechanical/pull/518>`__)
-  Bump ``pytest`` from 7.4.2 to 7.4.3
   (`#482 <https://github.com/ansys/pymechanical/pull/482>`__)
-  Bump ``tj-actions/changed-files`` from 39 to 40
   (`#477 <https://github.com/ansys/pymechanical/pull/477>`__)
-  Bump ``plotly`` from 5.17.0 to 5.18.0
   (`#478 <https://github.com/ansys/pymechanical/pull/478>`__)
-  Bump ``pandas`` from 2.1.1 to 2.1.4
   (`#481 <https://github.com/ansys/pymechanical/pull/481>`__,
   `#494 <https://github.com/ansys/pymechanical/pull/494>`__,
   `#525 <https://github.com/ansys/pymechanical/pull/525>`__)
-  Bump ``matplotlib`` from 3.8.0 to 3.8.2
   (`#488 <https://github.com/ansys/pymechanical/pull/488>`__,
   `#502 <https://github.com/ansys/pymechanical/pull/502>`__)
-  Bump ``sphinx-gallery`` from 0.14.0 to 0.15.0
   (`#509 <https://github.com/ansys/pymechanical/pull/509>`__)
-  Bump ``actions/labeler`` from 4 to 5
   (`#517 <https://github.com/ansys/pymechanical/pull/517>`__)
-  Bump ``actions/setup-python`` from 4 to 5
   (`#523 <https://github.com/ansys/pymechanical/pull/523>`__)

`0.10.4 <https://github.com/ansys/pymechanical/releases/tag/v0.10.4>`__ - 2023-10-06
====================================================================================

Dependencies
^^^^^^^^^^^^

-  Update ``ansys_mechanical_api`` from 0.1.0 to 0.1.1
   (`#444 <https://github.com/ansys/pymechanical/pull/444>`__)

`0.10.3 <https://github.com/ansys/pymechanical/releases/tag/v0.10.3>`__ - 2023-09-26
====================================================================================


Added
^^^^^

-  Set up daily run for 241 testing and added manual inputs for workflow
   dispatch (#385)
-  add option to include enums in global variables (#394)
-  add experimental libraries method (#395)
-  add nonblocking sleep (#399)
-  Add test case for exporting off screen
   image(`#400 <https://github.com/ansys/pymechanical/pull/400>`__)
-  Warn for obsolete apis (#409)


Fixed
^^^^^

-  Fix embedded testing for all python version in CI/CD
   (`#393 <https://github.com/ansys/pymechanical/pull/393>`__)
-  fix broken link (#397)
-  use Application.Exit() in 241+ (#396)
-  Fix stale globals by wrapping them (#398)
-  Fix API documentation (#411)
-  doc fix (#412)


Dependencies
^^^^^^^^^^^^

-  Bump ``sphinx`` from 7.2.5 to 7.2.6
   (`#403 <https://github.com/ansys/pymechanical/pull/403>`__)
-  Bump ``matplotlib`` from 3.7.2 to 3.8.0
   (`#404 <https://github.com/ansys/pymechanical/pull/404>`__
-  Bump ``imageio-ffmpeg`` from 0.4.8 to 0.4.9
   (`#405 <https://github.com/ansys/pymechanical/pull/405>`__
-  Bump ``ansys-sphinx-theme`` from 0.11.1 to 0.11.2
   (`#406 <https://github.com/ansys/pymechanical/pull/406>`__)
-  Bump ``plotly`` from 5.16.1 to 5.17.0
   (`#407 <https://github.com/ansys/pymechanical/pull/407>`__)
-  Bump ``docker/login-action`` from 2 to 3
   (`#408 <https://github.com/ansys/pymechanical/pull/408>`__)
-  Bump ``pyvista`` from 0.42.1 to 0.42.2
   (`#414 <https://github.com/ansys/pymechanical/pull/414>`__)

`0.10.2 <https://github.com/ansys/pymechanical/releases/tag/v0.10.2>`__ - 2023-09-08
====================================================================================

Added
^^^^^

-  Max parallel 2 for embedding tests - ci_cd.yml (#341)
-  New features for ansys-mechanical console script (#343)
-  Add a “Documentation and issues” section to README and doc landing
   page (#347)
-  Dependabot changelog automation (#354)
-  Follow up of dependabot automated changelog (#359)
-  Add license headers to files in src (#373)

Changed
^^^^^^^

-  Remove library-namespace from CI/CD (#342)
-  Bump grpcio from 1.56.2 to 1.57.0 (#349)
-  Bump plotly from 5.15.0 to 5.16.0 (#348)
-  Bump sphinxcontrib-websupport from 1.2.4 to 1.2.6 (#350)
-  Bump ansys-sphinx-theme from 0.10.2 to 0.10.3 (#351)
-  pre-commit autoupdate
   (`#362 <https://github.com/ansys/pymechanical/pull/362>`__),
   (`#380 <https://github.com/ansys/pymechanical/pull/380>`__),
   (`#391 <https://github.com/ansys/pymechanical/pull/391>`__)

Fixed
^^^^^

-  Fix private appdata issue (#344)
-  Fix issues with PyPIM object.inv location (#345)


Dependencies
^^^^^^^^^^^^

-  Bump ``plotly`` from 5.16.0 to 5.16.1
   (`#357 <https://github.com/ansys/pymechanical/pull/357>`__)
-  Bump ``sphinx`` from 7.1.2 to 7.2.5
   (`#358 <https://github.com/ansys/pymechanical/pull/358>`__,
   `#378 <https://github.com/ansys/pymechanical/pull/378>`__)
-  Bump ``sphinx-gallery`` from 0.13.0 to 0.14.0
   (`#361 <https://github.com/ansys/pymechanical/pull/361>`__)
-  Bump ``ansys-sphinx-theme`` from 0.10.3 to 0.11.1
   (`#360 <https://github.com/ansys/pymechanical/pull/360>`__,
   `#387 <https://github.com/ansys/pymechanical/pull/387>`__)
-  Bump ``pytest-print`` from 0.3.3 to 1.0.0
   (`#369 <https://github.com/ansys/pymechanical/pull/369>`__)
-  Bump ``tj-actions/changed-files`` from 37 to 39
   (`#367 <https://github.com/ansys/pymechanical/pull/367>`__,
   `#386 <https://github.com/ansys/pymechanical/pull/386>`__)
-  Bump ``imageio`` from 2.31.1 to 2.31.2
   (`#370 <https://github.com/ansys/pymechanical/pull/370>`__)
-  Bump ``pytest`` from 7.4.0 to 7.4.2
   (`#375 <https://github.com/ansys/pymechanical/pull/375>`__,
   `#389 <https://github.com/ansys/pymechanical/pull/389>`__)
-  Bump ``actions/checkout`` from 3 to 4
   (`#379 <https://github.com/ansys/pymechanical/pull/379>`__)
-  Bump ``imageio`` from 2.31.2 to 2.31.3
   (`#376 <https://github.com/ansys/pymechanical/pull/376>`__)
-  Bump ``sphinx-notfound-page`` from 1.0.0rc1 to 1.0.0
   (`#374 <https://github.com/ansys/pymechanical/pull/374>`__)
-  Bump ``pyvista`` from 0.42.0 to 0.42.1
   (`#388 <https://github.com/ansys/pymechanical/pull/388>`__)

`0.10.1 <https://github.com/ansys/pymechanical/releases/tag/v0.10.1>`__ - 2023-08-08
====================================================================================


Changed
^^^^^^^

-  Bump ansys-sphinx-theme from 0.10.0 to 0.10.2 (#337)
-  Update clr-loader dependency (#339)

`0.10.0 <https://github.com/ansys/pymechanical/releases/tag/v0.10.0>`__ - 2023-08-07
====================================================================================


Added
^^^^^

-  Added warning for ansys-mechanical when provided an input script
   (#319)
-  Add changelog check to CI/CD (#322)
-  Added version check for ansys-mechanical warning message (#323)
-  Added TempPathFactory to test_app_save_open (#332)

Changed
^^^^^^^

-  Update python minimum requirement from 3.7 to 3.8 (#333)
-  Minor private appdata updates (#335)


Fixed
^^^^^

-  Broken links (#316)
-  Remove project lock file on close (#320)
-  Fixed warning message for ansys-mechanical (#326)

`0.9.3 <https://github.com/ansys/pymechanical/releases/tag/v0.9.3>`__ - 2023-07-27
==================================================================================


Added
^^^^^

-  Add ansys-mechanical console script (#297)
-  addin configuration and tests (#308)


Changed
^^^^^^^

-  Bump matplotlib from 3.7.1 to 3.7.2 (#294)
-  Bump pyvista from 0.40.0 to 0.40.1 (#293)
-  Bump sphinx-autodoc-typehints from 1.23.0 to 1.23.3 (#284)
-  Bump patch version (#292)
-  Remove pkg-resources and importlib_metadata (#300)
-  Bump grpcio from 1.56.0 to 1.56.2 (#305)
-  Bump pyvista from 0.40.1 to 0.41.1 (#306)


Fixed
^^^^^

-  Update code snippet for accessing project directory. (#295)
-  Added import logging to doc file (#299)
-  Fix version variable issue running “ansys-mechanical -r {revn} -g”
   (#302)
-  Update wording in running_mechanical.rst (#303)

`0.9.2 <https://github.com/ansys/pymechanical/releases/tag/v0.9.1>`__ - 2023-07-07
==================================================================================


Added
^^^^^

-  Added private AppData functionality to embedding (#285)


Fixed
^^^^^

-  Updated pythonnet warning message (#286)


Changed
^^^^^^^

-  Bump pytest from 7.3.2 to 7.4.0 (#282)
-  Bump grpcio from 1.54.2 to 1.56.0 (#283)

`0.9.1 <https://github.com/ansys/pymechanical/releases/tag/v0.9.1>`__ - 2023-06-21
==================================================================================


Added
^^^^^

-  Add version configuration for embedding tests (#270)


Changed
^^^^^^^

-  Bump pytest-print from 0.3.1 to 0.3.2 (#273)


Fixed
^^^^^

-  FIX: Use updated ansys-tools-path to resolve - missing 1 required
   positional argument: ‘exe_loc’ issue (#280)

`0.9.0 <https://github.com/ansys/pymechanical/releases/tag/v0.9.0>`__ - 2023-06-13
==================================================================================


Added
^^^^^

-  link to pymechanical remote sessions examples (#252)
-  add doc to run script without embedding (#262)
-  pre-commit autoupdate (#269)


Changed
^^^^^^^

-  Bump ansys-sphinx-theme from 0.9.8 to 0.9.9 (#248)
-  Bump grpcio from 1.54.0 to 1.54.2 (#249)
-  Bump sphinx from 6.2.0 to 6.2.1 (#250)
-  change image tag in ci/cd (#254)
-  Bump pyvista from 0.39.0 to 0.39.1 (#256)
-  Standardizing data paths (#257)
-  Bump imageio from 2.28.1 to 2.30.0 (#258)
-  Bump pytest-cov from 4.0.0 to 4.1.0 (#259)
-  Bump imageio from 2.30.0 to 2.31.0 (#264)
-  Bump pytest from 7.3.1 to 7.3.2 (#267)
-  Bump plotly from 5.14.1 to 5.15.0 (#268)


Fixed
^^^^^

-  FIX: GitHub organization rename to Ansys (#251)
-  fix examples links (#253)
-  fix windows pythonnet warning unit tests (#260)

`0.8.0 <https://github.com/ansys/pymechanical/releases/tag/v0.8.0>`__ - 2023-05-12
==================================================================================

Added
^^^^^

-  changelog (#222)
-  add link to embedding examples (#228)
-  Add ``close()`` method to ``Ansys.Mechanical.Embedding.Application``.
   See (#229)
-  Add check if pythonnet exists in the user environment (#235)


Changed
^^^^^^^

-  cleanup docker ignore file (#206)
-  Update contributing.rst (#213)
-  Bump sphinx-autodoc-typehints from 1.22 to 1.23.0 (#215)
-  Bump pytest from 7.3.0 to 7.3.1 (#216)
-  Bump sphinx-gallery from 0.12.2 to 0.13.0 (#217)
-  Bump sphinx-copybutton from 0.5.1 to 0.5.2 (#218)
-  Bump sphinx-design from 0.3.0 to 0.4.1 (#219)
-  Remove python 3.7 (#230)
-  Use ansys-tools-path (#231)
-  Bump sphinx from 6.2.0 to 7.0.0 (#232)
-  Bump imageio from 2.28.0 to 2.28.1 (#233)
-  ignore generated *.ipynb,* .py, *.rst,* .md5, *.png and* .pickle
   files (#239)
-  Bump pyvista from 0.38.5 to 0.39.0 (#245)


Fixed
^^^^^

-  FIX: not necessary anymore to update apt-get (#220)
-  Include amd folder for mapdl solver in the docker image. (#200)
-  Remove jscript references from tests/ folder (#205)
-  Fixes the windows executable path for standalone mechanical (#214)
-  FIX: run_python_script\* return empty string for objects that cannot
   be returned as string (#224)
-  call ``new()`` in the BUILDING_GALLERY constructor of
   ``Ansys.Mechanical.Embedding.Application`` (#229)
-  fix documentation link (#234)
-  changed python doc url to fix doc pipeline error (#236)
-  Docker dependencies to support topo and smart tests (#237)

`0.7.3 <https://github.com/ansys/pymechanical/releases/tag/v0.7.3>`__ - 2023-04-20
==================================================================================


Changed
^^^^^^^

-  Reuse instance of embedded application when building example gallery
   (#221)

`0.7.2 <https://github.com/ansys/pymechanical/releases/tag/v0.7.2>`__ - 2023-04-13
==================================================================================


Changed
^^^^^^^

-  Bump plotly from 5.14.0 to 5.14.1 (#197)
-  Bump pytest from 7.2.2 to 7.3.0 (#196)
-  Bump peter-evans/create-or-update-comment from 2 to 3 (#195)
-  Bump ansys-sphinx-theme from 0.9.6 to 0.9.7 (#198)


Fixed
^^^^^

-  Fixed documentation for updating global variables (#203)
-  Remove references to unsupported legacy jscript APIs (#205)
-  Clean up docker image (#206, #200)

`0.7.1 <https://github.com/ansys/pymechanical/releases/tag/v0.7.1>`__ -  2023-04-10
===================================================================================

First public release of PyMechanical

.. vale on
