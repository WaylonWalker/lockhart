## 0.6.0

- fix: default to quiet console, make --verbose a common cli argument, #25 0.6.0.dev1
- fix: full test coverage in config #27 0.6.0.dev2
- fix: if default config is missing load in the sample config #27 0.6.0.dev2
- fix: config location was set to the sample by mistake #27 0.6.0.dev2
- Added console.log to print a message when no config file is
  found #29 0.6.0.dev4
- Add `get_jinja_env()` and support for templating and editing prompts in
  `prompts.py` #30 0.6.0dev5
- Added toggle_sidebar action. #32 0.6.0.dev7

## 0.5.0

- fix: do not run model if editor was closed without writing #7 0.4.0.dev2
- feat: add support for Edit mode #12 0.4.0.dev2
- feat: add support to jinja template all string type parameters #13 0.4.0.dev2
- feat: add --verbose flag #8 0.4.0.dev3
- feat: create history api, and save history #17 0.4.0.dev4
- fix: do not block for missing stdin #18 0.4.0.dev11
- feat: editor now opens full toml #20 0.4.0.dev12
