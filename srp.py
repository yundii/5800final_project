def irvings_algorithm(preferences):
    # Make deep copies of preferences for manipulation
    proposals = {k: v[:] for k, v in preferences.items()}
    current_engagements = {k: None for k in preferences.keys()}
    proposal_made = {k: None for k in preferences.keys()}
    proposal_accepted = {k: None for k in preferences.keys()}
    rejected = {k: set() for k in preferences.keys()}

    # Phase 1: Proposal Phase
    while any(proposal_made[ai] is None for ai in preferences.keys()):
        for ai in preferences.keys():
            if proposal_made[ai] is None:
                aj = next(p for p in proposals[ai] if p not in rejected[ai])

                if proposal_accepted[aj] is None:
                    proposal_accepted[aj] = ai
                    proposal_made[ai] = aj
                else:
                    ak = proposal_accepted[aj]
                    if proposals[aj].index(ai) < proposals[aj].index(ak):
                        proposal_made[ak] = None
                        proposal_accepted[aj] = ai
                        proposal_made[ai] = aj
                        rejected[ak].add(aj)
                    else:
                        rejected[ai].add(aj)

    # Phase 2: Rejection Phase
    for ai in preferences.keys():
        aj = proposal_accepted[ai]
        if aj is not None:
            ai_preferences = proposals[ai]
            for ak in ai_preferences[ai_preferences.index(aj) + 1:]:
                rejected[ai].add(ak)
                rejected[ak].add(ai)
                proposals[ak].remove(ai)
                proposals[ai].remove(ak)

    # Phase 3: Cycle Elimination Phase
    def find_cycle():
        for pi in preferences.keys():
            if len(proposals[pi]) > 1:
                qi = proposals[pi][1]  # second preference
                if len(proposals[qi]) == 0:
                    continue
                pi1 = proposals[qi][-1]  # last preference of qi

                cycle = [(pi, qi, pi1)]
                visited = {pi}
                while pi1 != cycle[0][0]:  # Check if a cycle is formed
                    if pi1 in visited:
                        break  # Prevent entering an infinite loop
                    visited.add(pi1)

                    pi = pi1
                    if len(proposals[pi]) <= 1:
                        break
                    qi = proposals[pi][1]

                    if len(proposals[qi]) == 0:
                        break
                    pi1 = proposals[qi][-1]
                    cycle.append((pi, qi, pi1))
                else:
                    print(f"Cycle found: {cycle}")
                    return cycle
        return None

    while True:
        cycle = find_cycle()
        if not cycle:
            break

        for pi, qi, pi1 in cycle:
            if pi1 in proposals[qi]:  # Ensure pi1 is still an option for qi
                proposals[qi].remove(pi1)
                proposals[pi1].remove(qi)
                rejected[qi].add(pi1)
                rejected[pi1].add(qi)

    # Prepare the final matches
    for ai in preferences.keys():
        if proposals[ai] is not None:
            current_engagements[ai] = proposals[ai][0]

    final_matches = {
        ai: aj for ai, aj in current_engagements.items() if aj is not None}

    return final_matches
