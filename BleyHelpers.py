# Copyright (c) 2009 Evgeni Golov <evgeni.golov@uni-duesseldorf.de>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import spf

def reverse_ip(ip):
    return spf.reverse_dots(ip)

def domain_from_host(host):
    d = host.split('.')
    if len(d) > 1:
       domain = '%s.%s' % (d[-2], d[-1])
    else:
       domain = host
    return domain

def is_dyn_host(host):
	host = host.lower()
	return host.find('dyn') != -1 or host.find('dial') != -1

def check_helo(params):
	if params['client_name'] != 'unknown' and params['client_name'] == params['helo_name']:
		score = 0
	elif domain_from_host(params['helo_name']) == domain_from_host(params['client_name']) or params['helo_name'] == '[%s]' % params['client_address']:
		score = 1
	else:
		score = 2
		
	if is_dyn_host(params['client_name']):
		score += 1

	spf_result = check_spf(params)
	if spf_result == -1:
		score += 1
	elif spf_result == 1:
		score -= 2

	print "Checked EHLO to score=%s" % score
	return score

def check_spf(params):
	s = spf.query(params['client_address'], params['sender'], params['helo_name'])
	r = s.check()
	if r[0] in ['fail', 'softfail']:
		return -1
	elif r[0] in ['pass']:
		return 1
	else:
		return 0
