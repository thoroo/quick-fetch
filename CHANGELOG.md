# Changelog

## 0.3.0

Major rewrite of code while maintaining same functionality but improved ways for user input. Now takes a instruction codebook (in json5 format) in which you write down stepwise instructions for either direct or indirect handling.

- Removed
    - Mode operations `Mouse` and `XPath`
- Changed
    - From multi config setup to now using only a single config for general settings
- Added
    - Better exception handling
    - Download file from a direct source (missing previously)
    - Use of instructions to download images/files

## 0.2.0

Restructured scripts while maintaning functionality.

- Changed
    - Moved `Mode` selection into config
- Added
    - Added option to disable sound
    - Added hotkey/URL validation with added exception handling
    - Added basic config validation
    - Added check for hostname match for navigation buttons

## 0.1.0

Initial commit with working version of project.

- Added
    - Download image directly
    - Download image indirectly
    - Download file directly
    - Download file indirectly
    - Ability to unzip files
    - Custom path for output
    - Mode selector
    - Config selector
    - Sounds for success, warning and errors
    - Clean and colorful console
    - Page navigator buttons, i.e. next and previous