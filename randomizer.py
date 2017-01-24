import random as r
import json
class randomizer(object):

	def gen_p_all_in_t(self):
		return r.randint(55, 75)
		
	def gen_p_raise_t(self):
		return r.randint(45, 65)

	def gen_p_call_t_one(self):
		return r.randint(1, 10)

	def gen_p_call_t_two(self):
		return r.randint(1, 15)

	def gen_p_bluff(self):
		return r.uniform(0.0, .12)

	def gen_f_check(self):
		return r.uniform(.5, .7)

	def gen_f_raise(self):
		return r.uniform(0,.5)

	def gen_f_bluff(self):
		return r.uniform(0, .1)

	def gen_r_check(self):
		return r.uniform(.5, .7)

	def gen_r_raise(self):
		return r.uniform(0,.5)

	def gen_r_bluff(self):
		return r.uniform(0,.1)

	def gen_s_check(self):
		return r.uniform(.5,.7)

	def gen_s_raise(self):
		return r.uniform(0,.5)

	def gen_s_bluff(self):
		return r.uniform(0,.1)

	def make_dicts(self, number_of_dicts):
		dicts = []
		for i in range(number_of_dicts):
			new = {
					"p_all_in_t":self.gen_p_all_in_t(),
					"p_raise_t":self.gen_p_raise_t(),
					"p_call_t_one":self.gen_p_call_t_one(),
					"p_call_t_two":self.gen_p_call_t_two(),
					"p_bluff":self.gen_p_bluff(),
					"f_check":self.gen_f_check(),
					"f_raise":self.gen_f_raise(),
					"f_bluff":self.gen_f_bluff(),
					"r_check":self.gen_r_check(),
					"r_raise":self.gen_r_raise(),
					"r_bluff":self.gen_r_bluff(),
					"s_check":self.gen_s_check(),
					"s_raise":self.gen_s_raise(),
					"s_bluff":self.gen_s_bluff()
					}
			dicts.append(new)
		return dicts


hehe = randomizer()
params = hehe.make_dicts(100)

f = open('randp.txt', 'w')
f.write(json.dumps(params))
f.close()
