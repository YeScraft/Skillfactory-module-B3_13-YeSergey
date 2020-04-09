import sys

class Tag:
    def __init__(self, tag, klass=None, toplevel=False, is_single=False, **kwargs):
        self.tag = tag
        self.text = "aaa"
        self.attributes = {}
        self.id = ""
        self.src = ""
        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value
    
    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(' %s = "%s"'%(attribute, value))
        attrs = " ".join(attrs)
        
        if self.children:
            unTop = ""
            unTop = unTop + "  <{tag}{attrs}>\n".format(tag=self.tag, attrs = attrs)          
            for child in self.children:
                unTop = unTop + "  "+str(child)+"\n"
            return unTop + "  </%s>"%self.tag
        else:
            if self.is_single:
                return "  <{tag}{attrs}>".format(tag=self.tag, attrs = attrs)
            else:
                return "  <{tag}{attrs}>{text}</{tag}>".format(tag=self.tag, attrs = attrs, text=self.text)
 
class HTML(Tag):
    def __init__(self, output):
        self.tag = "html"
        self.output = output
        self.attributes = {}
        self.children = []
        lines = []
        
    def __enter__(self):
        return self
    
    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is None:
            print(self)
        else:
            with open(self.output, "w") as fp:
                fp.write(str(self))
                
    def __str__(self):
        html = "<%s>\n"%self.tag
        for child in self.children:
            html = html + str(child)+"\n"
        html = html + "</%s>"%self.tag
        return html
               
class TopLevelTag(HTML):
    def __init__(self, tag):
        self.tag = tag
        self.children = []
        self.attributes = {}
        self.text = ""

    def __enter__(self):
        return self
    
    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, *args, **kwargs):
        return self
          
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(" %s = %s"%(attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            Top = ""
            Top = Top + "<{tag}{attrs}>\n".format(tag=self.tag, attrs = attrs)         
            for child in self.children:
                Top = Top + str(child)+"\n"
            return Top + "</%s>"%self.tag
        else:
            return Top +("<{tag}{attrs}>{text}</{tag}>".format(tag=self.tag, attrs = attrs, text=self.text))

def main(output=None):
    with HTML(output=output) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head
        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1
            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph
                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img
                body += div
            doc += body
if __name__ == "__main__":
    output=None
    if len(sys.argv) > 1:# Выбор вывода: на экран или в файл, если указано имя.
        main(output = sys.argv[1])
    else:
        main()
    
""" 
Запуск в cmd:
"python homework.py"               - для вывода на экран,
"python homework.py filename.html" - для записи в файл."""
#output="test.html"   
