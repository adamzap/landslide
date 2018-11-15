# Changelog

## v1.1.6

- Fix packaging again

## v1.1.5

- Fix packaging

## v1.1.4

- Setup Travis CI
- Update Python versions in `setup.py`
- Pin dependency versions to fix `markdown` issue

## v1.1.3

- Identify each slide by a numbered class (#171) (dkg)
- Fix theme image embedding regex to grab all images (#170)
- Fix blockquote font size for rst (#161)
- Fix display of RST image target links (#87)
- Fix relative path generation (#147)
- Add command line option for print version (#135)
- Add use of '---' as a slide separator to textile files (#163)
- README improvements (#88 and #101)
- Improve image path regex and replacement (#177)

## v1.1.2

- Add support for Python 3
- Allow support for copy_theme argument in CFG files (#139) (syscomet)
- Improve MathJax rendering for Markdown files
- Support math output (#144) (davidedelvento)
- Allow presenter notes in slides with no heading in RST files (#141) (regebro)
- And more...

## v1.1.1

### Fixes

- Don't accidentally require watchdog (#134)

## v1.1.0

### Major Enhancements

- Add CHANGELOG
- Add "ribbon" theme from "shower" presentation tool (#129) (durden)
- Add `-w` flag for watching/auto-regenerating slideshow (#71, #120) (jondkoon)

### Minor Enhancements

- Supress ReST rendering errors
- CSS pre enhancements (#91) (roktas)
- Add an example using presenter notes (#106) (netantho)
- Run macros on headers also, to embed images (#74) (godfat)
- Allow PHP code snippets to not require <?php (#127) (akrabat)
- Allow for line numbers and emphasis with reStructuredText (#97) (copelco)
- Add an option to strip presenter notes from output (#107) (aaugustin)

### Fixes

- Firefox offset bug on next slide (#73)
- Fix base64 encoding issue (#109) (ackdesha)
- Fix to embed images defined in CSS (#126) (akrabat)
- Minor documentation fixes (#119, #131) (durden, spin6lock)
- Use configured encoding when reading all embedded files (#125) (iguananaut)
- Allow pygments lexer names that include special characters (#123) (shreyankg)
