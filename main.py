import dealer
from agents import *
from simulators import *


def call_dealer():
	players_count = 2
	simulation_count = 10

	simulator_obj = tictactoesimulator.TicTacToeSimulatorClass(num_players = players_count)

	agent_one = randomagent.RandomAgentClass(simulator = simulator_obj)
	agent_two = uniformagent.UniformRolloutAgentClass(simulator = simulator_obj, rollout_policy = agent_one, pull_count = 5)
	#agent_three = uniformagent.UniformRolloutAgentClass(simulator = simulator_obj, rollout_policy = agent_two, pull_count = 3)

	agents_list = [agent_one,agent_two]
	dealer_object = dealer.DealerClass(agents_list, simulator_obj, num_simulations = simulation_count)
	dealer_object.start_simulation()
	results = dealer_object.simulation_stats()

	# RESULTS CALCULATION
	overall_reward = []
	for game in xrange(len(results)):
		reward_sum = [0] * players_count

		for move in xrange(len(results[game])):
			reward_sum = [x + y for x, y in zip(reward_sum, results[game][move][0])]

		for x in xrange(len(reward_sum)):
			reward_sum[x] = reward_sum[x] / len(results[game])

		# print "REWARD AVG FOR EACH AGENT IN GAME {0} : ".format(game)
		# print reward_sum
		overall_reward.append(reward_sum)

	overall_reward_avg = [0] * players_count
	for game in xrange(len(results)):
		overall_reward_avg = [x + y for x, y in zip(overall_reward_avg, overall_reward[game])]

	for x in xrange(len(overall_reward_avg)):
		overall_reward_avg[x] = overall_reward_avg[x] / simulation_count

	print "REWARD AVG FOR OVERALL SIMULATION : "
	print overall_reward_avg

if __name__ == "__main__":
	call_dealer()