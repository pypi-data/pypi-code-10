#!/usr/bin/python3

""" This is just a very basic module to find a specific prime number. This is my first python program. Everything I do and plan to do is CC-BY-SA. Thanks for stopping by. Alpha32
"""

how_high = int(input("Enter the range: "))
nth_prime = int(input("Enter the prime to find: "))

def find_a_prime(nth_prime, how_high):

	primes = [1,3,5,7]	
""" I did this because I ran into issues getting the single-digit primes to show up.
 If you have a better solution, let me know.
"""

	for i in range(10, how_high):
		if i%2==0:
			continue
		elif i%3==0:
			continue
		elif i%5==0:
			continue
		else:
			primes.append(i)
	
	print(primes[nth_prime]) 

if __name__ == '__main__':
	find_a_prime(nth_prime, how_high)
