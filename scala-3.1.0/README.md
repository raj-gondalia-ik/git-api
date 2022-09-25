Downloaded from
https://github.com/lampepfl/dotty/releases/download/3.1.0/scala3-3.1.0.tar.gz

The following local changes are made in the downloaded version:
* Ran `sed -i 's/JAVACMD...../JAVACMD\\"" " $JAVA_OPTS /g' bin/scala` to make bin/scala respect $JAVA_OPTS env variable (as Scala 2 did).
  * This change is made by Sphere Engine in their production, so we are matching it in our test environment.
  * Committed as 21b30121bcc
* On 2022/03/23 some `.jar` files that we don't seem to use have been removed.
  * Reason: reduce repository size.
  * Committed as 18d67836c54
* Patched exit code in MainGenericRunner.scala (scala3-compiler_3-3.1.0.jar) as mentioned in https://github.com/lampepfl/dotty/issues/15022 on 2022/04/25
  * Committed as ad0cbe5a828b8a8

