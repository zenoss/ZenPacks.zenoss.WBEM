DIST_DIR=../dist
OUTPUT_HTML=$(DIST_DIR)/README.html

docs:
	test -d $(DIST_DIR) || mkdir $(DIST_DIR)
	pandoc body.md --template=template.html --table-of-contents > $(OUTPUT_HTML)

