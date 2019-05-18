%%%-------------------------------------------------------------------
%%% @author bj
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 18. 5月 2019 21:47
%%%-------------------------------------------------------------------
-module(bjtalk_server).
-author("bj").

%%-behavior(gen_server).

%% API
-export([
%%  start_link/0,
%%  init/1
  start/0
]).

%%start_link() ->
%%  gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).
%%
%%init([]) ->
%%
%%  {ok, []}.

start() ->
  {ok, Socket} = gen_udp:open(27010, [binary]),
  io:format("start bjtalk server~n"),
  loop(Socket, #{}).

loop(Socket, Users) ->
  io:format("start bjtalk server loop~n"),
  receive
    {udp, Socket, Host, Port, Bin} ->
      io:format("recv:~p~n", [Bin]),
      User = {Host, Port},

      case maps:is_key(User, Users) of
        true ->
          io:format("~p ~p active~n", [Host, Port]),
          maps:get(User, Users) ! {ping},
          broadcast(Socket, maps:keys(Users) -- [User], Bin),
          loop(Socket, Users);

        false ->
          io:format("~p ~p connect~n", [Host, Port]),
          broadcast(Socket, maps:keys(Users), Bin),
          Self = self(),
          Sup = spawn(fun() -> sup_user(User, Self) end),
          loop(Socket, Users#{User => Sup})
      end;

    {timeout, User} ->
      io:format("remove:~p~n", [User]),
      loop(Socket, maps:remove(User, Users))
  end.

send(Socket, User, Bin) ->
  {Host, Port} = User,
  gen_udp:send(Socket, Host, Port, Bin).

broadcast(Socket, Users, Bin) ->
  case Bin of
    <<"ping">> ->
      ok;
    _ ->
      lists:map(fun(U) -> send(Socket, U, Bin) end, Users)
  end.

sup_user(User, Master) ->
%%  {Host, Port} = User,
%%  gen_udp:send(Socket, Host, Port, <<"ping">>),
  receive
    {ping} ->
      sup_user(User, Master)
  after 5000 ->
    Master ! {timeout, User}
  end.

