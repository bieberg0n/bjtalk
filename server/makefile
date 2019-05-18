main:
	rebar3 compile

run:
	rebar3 compile
	erl -noshell -pa _build/default/lib/bjtalk/ebin/ -s bjtalk_server start -s init stop
