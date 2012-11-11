# Changelog

A log of changes to Landslide that are worth mentioning

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
