JARPATH := target/scala-2.13/liquid-assembly-0.1.jar

update:
	cd ../liquid; sbt assembly
	cp ../liquid/$(JARPATH) $(JARPATH)
