#Copyright 2019 Jory Lafaye - GPL-3.0-or-later
#
#This file is part of Karmic-client.
#
#    Karmic-client is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Karmic-client is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Karmic-client.  If not, see <https://www.gnu.org/licenses/>.

import builtins
import time
from datetime import datetime

file = open('data/karmic-client.log', 'a')

def printLog(message):
    date = str(datetime.fromtimestamp(time.time()).strftime('%d/%m/%y - %Hh %Mm %Ss'))
    toPrint = date+": "+str(message)
    print(toPrint)
    file.write(toPrint+"\n")

globals()['__builtins__']["printLog"] = printLog
