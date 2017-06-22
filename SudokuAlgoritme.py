# Sudoku algoritm

min_conflicts(puzzle, iteration_limit, acceptance_probability):
    tabu_list = []
    iteration_counter = 0
    best_cost = 0
    current_cost = MAX

    while best_cost > 0 and iteration_counter < interation_limit:
        randomly select cell which is in conflict
        generate all prossible swaps with the selected cell

        best_swap = find the best swap which minimalizes total conflicts
        best_swap_not_tabu = find the best swap which minimizes total conflicts and is not tabu

        if best_swap /= best_swap_not_tabu:
            if evaluate(best_swap) < best_cost:
                current_cost = evaluate(best_swap)
                perform swap
                go to 27
        if evaluate(best_swap_not_tabu) < current_cost and random() = acceptance_probability:
            current_cost = evaluate(best_swap)
            perform swap

        update tabu list
        if current_cost < best_cost:
            best_cost = current_cost
            iteration_count = 0
        else:
            iteration_count = iteration_count + 1

local_search(puzzle, time_limit, reset_factor, alpha):
    fix_cells_using_arc_consistency(puzzle)
    fill_remaining_cells_randomly(puzzle)

    best_puzzle = puzzle
    best_cost = evaluate(puzzle)

    while best_cost > 0 and time_limit is not passed:
        puzzle = min_conflicts_with_tabu_list(puzzle)
        cost = evaluate(puzzle)

        if best_cost > cost:
            best_cost = cost
            best_puzzle = puzzle

        if cost > 0:
            empty all unfixed cells in puzzle which are in conflict

            additionally empty relative ammount of
            remaining unfixed cells defined by reset_factor

            forward_checking_search(puzzle)

            fill_remaining_cells_randomly(puzzle)

            reset_factor = reset_factor * alpha
