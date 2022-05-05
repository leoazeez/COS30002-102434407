''' Towers of Hanoi as State Graph Search

Created for COS30002 AI for Games, Lab,
by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without
permission.

This is a classic mathematical puzzle credited to the French mathematician
Édouard Lucas in 1883. (See https://en.wikipedia.org/wiki/Tower_of_Hanoi)

Consider a situation of three poles (or stacks), and a number (n) of disks of
different unique sizes.

The puzzle starts with all disk stacked and ordered on the first pole with the
biggest at the bottom, and the smallest at the top.

Here is a simple text based representation of the start state with only three
disks (n=3).

    |       |       |
   *|*      |       |
  **|**     |       |
 ***|***    |       |

The goal (end state) is to move all the disks from the starting pole to a
target pole while following three simple rules:
1. you can only move one disk at a time
2. you can only move the top disk from a pole
3. you can not put a larger disk on top a smaller disk.

The problem can be solved using both iterative and recursive approaches.
Because of this, it is a classic teaching example for recusion in programming
subjects around the world.

The minimal number of moves to solve a puzzle like this is 2^n - 1.
So for 3 disks it takes, 2^3 -1 = 2*2*2 - 1 = 8 - 1 = 7
(In python maths, power is writen as ** and so expressed as moves = 2**3 -1 )

Our objective is this unit is to use the puzzle as a state-based system
represented as a search graph (tree), and is a good basis for later
uses of graphs and graph search for problem solving and AI for Games.

Because of this, we will start first with a verbose iterative approach.

2019-03-15 Initial version.

'''


def init_poles(disks):
    '''Return the three poles as a list of list.
    The first list contains the number of disks, with the biggest disk at the
    bottom (index 0) up to the smallest (index disks-1).
    Note: The smallest disk size is 1, not 0.
    '''
    result = [
        [], # first (source)
        [], # second (helper)
        [], # third (target)
    ]
    # want size 1 not 0, but it would work anyway
    # setting disks in pole 1 (the source), for disks=3 the result would be
    # [[3,2,1],[],[]] 
    result[0] = list(range(disks, 0, -1))
    return result


def print_poles(poles):
    ''' Simple view with one pole per line, each a list str
    For n=7, looks something like
    ---poles---
    0 : [7, 6, 5, 4, 3, 2, 1]
    1 : []
    2 : []
    '''
    print('---poles---')
    for i, p in zip(list(range(len(poles))), poles):
        print(i, ':', p)


def print_poles_as_state(poles, test_valid=False):
    ''' Single line as a "state"
    Example (with test_valid=False):
        State: ([7, 6, 5, 4, 3, 2, 1],[],[])
    '''
    if poles is None:
        print('States: Not valid')
    else:
        result = '(%s)' % ','.join([str(p) for p in poles])
        if test_valid:
            print('State:', result, is_valid_state(poles))
        else:
            print('State:', result)


def print_poles_as_text(poles, n):
    '''Show a fancy :) text-based graphical representation.
    '''
    # Note: Having n makes this easier to space width (without searching for
    # biggest value, which is possible but wasted effort.)

    # Print from the top down
    for i in range(n-1, -1, -1):
        line = ''
        for p in range(len(poles)):
            v = '*' * poles[p][i] if len(poles[p]) > i else ''
            line += "%*s|%-*s " % (n, v, n, v)
        print(line)


def is_valid_state(poles):
    ''' Check that each pole only has big-small size from bottom to top.
    Returns True if all poles are okay, or False if one is.
    - Will work with any number of poles.
    - Does not check for multiple disk of same size.
    '''
    # for each pole in poles (source pole, helper pole, and target pole), we sort the disks of the pole 
    # from the biggest to the smallest (that's why we used reverse inside sort)
    # if the pole is different from the sorted pole, the state is not valid (the function returns False),
    # but if the pole equals the same pole sorted (which means that the pole was already sorted), the state is 
    # valid and the function returns True.
    # we return False as soon as we find a non sorted pole, for example if the source pole is not already sorted
    # the function returns False (the state is invalid), so the function return valid only in one case,
    # and that case is when all the poles are valid (sorted). 
    for p in poles:
        if sorted(p, reverse=True) != p:
            return False  # no need to wait
    return True


def move_disk(poles, src, dest):
    #print("we are inside move disk")
    print("(Moving  Disk) plos =={} src={} dest={}".format(poles,src,dest))
    ''' Move a single disk from the src pole to the dest pole.
    - src or dest = pole index, i.e. 0, 1, 3
    - Does check if there is a piece to move, returns None if not.
    - Does NOT check if it is a valid state, just does the move.
    - Does NOT modify poles - returns a copy with change
    '''
    # check if it's a valid move
    if poles[src]:
        result = copy_state(poles)
        #print("result before::", result)
        #print("rsult[src]=", result[src])
        result[dest].append(result[src].pop(-1))
        #print("result after::", result)
        return result
    else:
        return None


def copy_state(poles):
    '''Perform a "deep" copy of poles'''
    return [p.copy() for p in poles]


def state_as_tuple(poles):
    '''Return an immutable tuple version of the list of lists.
    The pole state can then be used as a key for a dict's which is handy.
    '''
    result = tuple(tuple(p) for p in poles)
    #print(result)
    return result


def solve_using_recursion(n):
    # make moves available as a list for later...
    moves = []
    # This is the recursively called "move" function
    def move(n, src, dest, aux):
        if n>0:
            move(n-1,src,aux,dest)
            moves.append((src,dest))
            move(n-1,aux,dest,src)
        print("moves ::: ", moves)

    # generate the recursive sequence stored in moves
    print('Generating set of moves for %d (2^n - 1 = %d) disks using recusion ... ' % (n, 2**n -1))
    move(n, 0, 2, 1) # standard 3-pole configuration
    print('- moves (%d): %s' % (len(moves), moves) )

    # check if it worked?
    if not moves:
        print("Eh? No moves generated! Did you fix the move function?")
        return

    # create the initial state, then do the "moves" found recursively
    s = init_poles(n)
    print_poles_as_text(s, n)
    for src, dest in moves:
        print('> Moving from', src, 'to', dest)
        s = move_disk(s, src, dest)
        print_poles_as_text(s, n)
        #print(is_valid_state(s))
        print_poles_as_state(s, test_valid=True)
    print('Done.')


def attempt_using_random_moves(n, limit):
    print("Guessing with n=%d, limit=%d ..." % (n, limit))
    s_start = init_poles(n)
    s_end = copy_state(s_start)
    #s_end[-1] is the last of s_end
    s_end[0], s_end[-1] = s_end[-1], s_end[0]

    cache = {}  # of states seen (not moves)
    #print(cache)
    history = []  # of moves, not state outcomes

    from random import sample, seed
    #seed(1234)

    s = s_start
    history.append((-1,-1)) # fake first move

    status = 'Running'
    count = 0
 
    while status == 'Running':
        # Found it?
        if s == s_end:
            status = 'Found it!'
            
        elif count >= limit:
            status = 'Hit Limit. No solution.'
            
        else:
            # Default pointless move
            #src, dest = 0, 0
            #random move
            src, dest = sample([0,1,2],2)
            
            # What is the new state using the random src and desk poles
            # - This might return None if move not valid (no src disk exists to move)
            new_s = move_disk(s, src, dest)
            #print_poles_as_state(new_s)

            # Is the new state valid? only keep it if it is ...
            if new_s:
                ### TODO: extension  test/add to cache here to avoid loops
                valid = is_valid_state(new_s)
                # if new state is valid, keep it
                if valid:
                    s = new_s
                    history.append((src, dest))
        count += 1
        #print("history = {} count={}".format(history,count))

    # remove first fake move (keeps things pretty)
    history.pop(0) # (-1,-1)
    # Show results, more details if there isn't too many to show ...
    print('Result:', status)
    print('Count (attempted random moves)', count-1)
    if (status == 'Found it!') and (len(history) < 200):
        print(history)
    print('Moves (valid and kept):', len(history))
    print('Done.')
    return [status == 'Found it!', history]

def attempt_using_random_moves2(n, limit):
    print("Guessing with n=%d, limit=%d ..." % (n, limit))
    s_start = init_poles(n)
    s_end = copy_state(s_start)
    #s_end[-1] is the last of s_end
    s_end[0], s_end[-1] = s_end[-1], s_end[0]

    cache = {}  # of states seen (not moves)
    #print(cache)
    history = []  # of moves, not state outcomes

    from random import sample, seed
    #seed(1234)

    s = s_start
    history.append((-1,-1)) # fake first move

    status = 'Running'
    count = 0
 
    while status == 'Running':
        # Found it?
        if s == s_end:
            status = 'Found it!'
            
        elif count >= limit:
            status = 'Hit Limit. No solution.'
            
        else:
            # Default pointless move
            #src, dest = 0, 0
            #random move
            _src,_dest = history[-1]
            src, dest = sample([0,1,2],2)
            if(src!=_dest) or (dest!=_src):
                print("last move reversal detected")
                print("_src:{} src:{} _dest:{} dest:{}".format(_src,src,_dest,dest)) 
                break
            # What is the new state using the random src and desk poles
            # - This might return None if move not valid (no src disk exists to move)
            new_s = move_disk(s, src, dest)
            #print_poles_as_state(new_s)

            # Is the new state valid? only keep it if it is ...
            if new_s:
                ### TODO: extension  test/add to cache here to avoid loops
                valid = is_valid_state(new_s)
                # if new state is valid, keep it
                if valid:
                    s = new_s
                    history.append((src, dest))
        count += 1
        #print("history = {} count={}".format(history,count))

    # remove first fake move (keeps things pretty)
    history.pop(0) # (-1,-1)
    # Show results, more details if there isn't too many to show ...
    print('Result:', status)
    print('Count (attempted random moves)', count-1)
    if (status == 'Found it!') and (len(history) < 200):
        print(history)
    print('Moves (valid and kept):', len(history))
    print('Done.')
    return [status == 'Found it!', history]



if __name__ == "__main__":

    ### 1 Simple test section.
    
    if True:
        print("start")
        # setup
        n = 7
        s1 = init_poles(n)
        # try each type of print
        print_poles(s1)
        print_poles_as_state(s1)
        print_poles_as_text(s1, n)
        # test for valid first state
        print(is_valid_state(s1))

        # move first disk
        s2 = move_disk(s1, 0, 2)
        print_poles_as_text(s2, n)
        print(is_valid_state(s2))

        # do an invalid move
        s3 = move_disk(s2, 0, 2)
        print_poles_as_text(s3, n)
        print(is_valid_state(s3))

        # do a valid second move
        s3 = move_disk(s2, 0, 1)
        print_poles_as_text(s3, n)
        print(is_valid_state(s3))
        print("end")

    ### 2 Perform a sequence of moves
    if True:
        # do a sequence of moves
        print("Running coded sequence ...")
        n = 3
        s = init_poles(n)
        print_poles_as_text(s, n)
        ### 3.
        moves = [(0, 2), (0, 1), (2, 1), (0, 2), (1, 0), (1, 2), (0, 2)]
        for src, dest in moves:
            print('> Moving from', src, 'to', dest)
            s = move_disk(s, src, dest)
            print_poles_as_text(s, n)
            print("is valid :: ",is_valid_state(s))
            print_poles_as_state(s, test_valid=True)
        print('Done.')

    ### 4 Try to find the solution using random (but valid) guesses for each move
    if True:
        attempt_using_random_moves(n=3, limit=100)
        attempt_using_random_moves(n=3, limit=200)
        
    if True:
        counter=0
        seq_lengths = []
        #results found starting from nb_attempts=200 using sample (random)
        #attempt_using_random_moves(n=3, limit=200)

        # statistics for 10 runs (the times the puzzle was solved with limit=100, and the lenghts of
        # the sequences of the solutions)
        for elem in range(10):

            #Step 4. incomment res = attempt_using_random_moves2(n=3, limit=100) to execute step4
            #res = attempt_using_random_moves2(n=3, limit=100)

            res = attempt_using_random_moves(n=3, limit=100)
            if(res[0]):
                counter+=1
                seq_lengths.append(len(res[1]))
        
        print("in 10 runs, the puzzle was solved {} times, and the lenghts of sequences are {}".format(
            counter,seq_lengths))

    ### 5 Generate the recursive sequence of moves
    if True:
        solve_using_recursion(n=3)
        print("Trying Recursion with number of sisks == 5\n")
        solve_using_recursion(n=5)
