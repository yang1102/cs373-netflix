FILES :=                              \
    Netflix.html                      \
    Netflix.log                       \
    Netflix.py                        \
    RunNetflix.in                     \
    RunNetflix.out                    \
    RunNetflix.py                     \
    TestNetflix.out                   \
    TestNetflix.py                    
   	# Netflix-tests/sy6955-RunNetflix.in   \
   	# Netflix-tests/sy6955-RunNetflix.out  \
   	# Netflix-tests/sy6955-TestNetflix.out \
   	# Netflix-tests/sy6955-TestNetflix.py  

ifeq ($(CI), true)
    COVERAGE := coverage
    PYLINT   := pylint
else
    COVERAGE := coverage-3.5
	PYLINT   := pylint3
endif

.pylintrc:
	$(PYLINT) --disable=bad-whitespace,missing-docstring,pointless-string-statement --reports=n --generate-rcfile > $@

Netflix-tests:
	git clone https://github.com/cs373-summer-2016/Netflix-tests.git

Netflix.html: Netflix.py
	pydoc3 -w Netflix

Netflix.log:
	git log > Netflix.log

RunNetflix.tmp: .pylintrc RunNetflix.in RunNetflix.out RunNetflix.py
	-$(PYLINT) Netflix.py
	-$(PYLINT) RunNetflix.py
	./RunNetflix.py < RunNetflix.in > RunNetflix.tmp
	python3 -m cProfile RunNetflix.py < RunNetflix.in > RunNetflix.tmp
	cat RunNetflix.tmp

TestNetflix.tmp: .pylintrc TestNetflix.py
	-$(PYLINT) Netflix.py
	-$(PYLINT) TestNetflix.py
	$(COVERAGE) run --branch --omit=*numpy* TestNetflix.py >  TestNetflix.tmp 2>&1
	$(COVERAGE) report -m       >> TestNetflix.tmp
	cat TestNetflix.tmp

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  .pylintrc
	rm -f  *.pyc
	rm -f  Netflix.html
	rm -f  Netflix.log
	rm -f  RunNetflix.tmp
	rm -f  TestNetflix.tmp
	rm -rf __pycache__
	rm -rf Netflix-tests

config:
	git config -l

format:
	autopep8 -i Netflix.py
	autopep8 -i RunNetflix.py
	autopep8 -i TestNetflix.py

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: Netflix.html Netflix.log RunNetflix.tmp TestNetflix.tmp Netflix-tests check


