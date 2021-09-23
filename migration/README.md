# Migration notes

Details of testing migration between Slaw and Bluebell.

* `constitution-slaw.xml`: the constitution, in slaw format (source)
* `constitution-bluebell.xml`: the constitution, in bluebell format (target)

## Creating the target for comparison purposes

1. Apply XSLT to convert the source document to bluebell-ready XML: `xsltproc slaw-to-bluebell.xslt constitution-slaw.xml > constitution-slaw-for-bluebell.xml`
2. Apply XSLT to unparse the intermediate document into bluebell text: `xsltproc ../bluebell/akn_text.xsl constitution-slaw-for-bluebell.xml > constitution-slaw-for-bluebell.txt`
3. Parse the bluebell text into bluebell XML: `python ../bin/bluebell /akn/za/act/1996/constitution act constitution-slaw-for-bluebell.txt > constitution-bluebell.xml`
4. Make it pretty for debugging purposes (optional): `cat constitution-bluebell.xml | xmllint --pretty 1 - > constitution-bluebell-pretty.xml`

## Comparing the two

There are some expected differences between the two documents, such as eId differences. We want to remove those
so that we can use a diff tool to see what the other differences are.

Generate prettified versions of the source and target documents:

1. `xsltproc for-comparison.xslt constitution-slaw.xml | xmllint --pretty 1 - > constitution-slaw-comparison-pretty.xml`
2. `xsltproc for-comparison.xslt constitution-bluebell.xml | xmllint --pretty 1 - > constitution-bluebell-comparison-pretty.xml`

Now compare `constitution-slaw-comparison-pretty.xml` and `constitution-bluebell-comparison-pretty.xml` in a diff tool.

In PyCharm, select the two files and use Ctrl-D (right click, Compare Files).

## Notes

* still need to correctly convert old-style crossheadings to new styles
* still need to handle use of crossheadings as subheadings in attachments
