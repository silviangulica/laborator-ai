temp_state = transition(state, move)
            pred_move, score_pred = choose_a_move_minimax_predicted(temp_state)

            print("Move: ", move, "Score: ", score)
            print("Move predict: ", pred_move, "Score: ", score_pred)
            if abs(score_pred) > abs(score):
                move = pred_move