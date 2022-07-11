require 'mp'
require 'mp.msg'

local socket = require "socket"
local udp = socket.udp()

udp:settimeout(0)
udp:setoption('reuseaddr',true)
udp:setsockname('*', 1900)
udp:setpeername('127.0.0.1', 5000) -- Echo IP and Port number

local function divmod(a, b)
	return a / b, a % b
end

local old_time
local function copyTime()
	local time_pos = mp.get_property_number("time-pos")
	if time_pos ~= nil then  
		local minutes, remainder = divmod(time_pos, 60)
		local hours, minutes = divmod(minutes, 60)
		local seconds = math.floor(remainder)
		local milliseconds = math.floor((remainder - seconds) * 1000)
		local time = string.format("%02d:%02d:%02d", hours, minutes, seconds)
		if old_time ~= time then
			old_time = time
			udp:send(string.format("%s", time))
		end 
	end
end

function on_pause_change(name, value)
	copyTime();
end

mp.observe_property("time-pos", "number", on_pause_change)
