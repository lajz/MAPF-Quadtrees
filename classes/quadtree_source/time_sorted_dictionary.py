from collections import deque


class TimeSortedDictionary:

    # elements is a sorted array of positions
    # turn on should use deque if more times in modal change than agents are going to be added
    def __init__(self, time_step=0.5, should_use_deque=False):
        self.time_step = time_step
        self.should_use_deque = should_use_deque
        if not self.should_use_deque:
            # list is kept in reverse order as there will be more changes to the front of the list than the rear
            self.ordered_times = []
        else:
            # use deque if more changes to start of array then middle
            self.ordered_times = deque()
        self.dict = {}
        # initialize start and end time to -1 to signify that they have not been det
        self.start_time = -1
        self.end_time = -1

    # return ordered times in ascending order, this requires reversing the list if it is reversed
    def get_ordered_times(self):
        if not self.should_use_deque:
            temp_times = self.ordered_times.copy()
            temp_times.reverse()
            return temp_times
        else:
            return list(self.ordered_times)

    # get dictionary value by index, uses ordered times get by index, and uses that as key in dictionary
    def dict_index(self, index):
        if index >= len(self.ordered_times):
            print("error index greater than ordered times lengths")
            return
        if self.should_use_deque:
            return self.dict[self.ordered_times[index]]
        else:
            dict_key = self.ordered_times[len(self.ordered_times) - 1 - index]
            return self.dict[dict_key]

    # change start time of model creating quadtree nodes if it is before current start, and deleting quadtree nodes if
    # it is after current start
    def change_start_time(self, new_start_time, new_quad_tree_node):
        # in special case of model not having start and end times initialized yet set start and end times are set and
        # first end time at this start time is created
        if self.start_time == -1 and self.end_time == -1:
            self.start_time = new_start_time
            self.end_time = new_start_time
            # NOT NEEDED CREATES AN EXTRA NODE AT THIS NEW START TIME
            # if self.should_use_deque:
            #     self.ordered_times.appendleft(new_start_time)
            # else:
            #     self.ordered_times.append(new_start_time)
            # self.dict[new_start_time] = new_quad_tree_node(new_start_time)
            return

        # store start time to calculate time changes
        old_start_time = self.start_time
        if new_start_time > self.end_time:
            print("error start time is greater than end time")
            return

        # calculate difference to see how many quadtrees must be created
        diff = self.end_time - new_start_time

        # if difference is multiple of time step then use that start time, otherwise make it multiple on larger side
        if diff % self.time_step == 0:
            self.start_time = new_start_time
        else:
            # recalculate difference
            diff = (((diff // self.time_step) + 1) * self.time_step)
            # calculate new start time from difference
            self.start_time = self.end_time - diff

        # if start time did not change than we don't need to do anything
        if self.start_time == old_start_time:
            return
        # if start time has increased  then we must remove unnecessary quadtrees
        if self.start_time > old_start_time:
            for index in range(0, round((self.start_time - old_start_time)/self.time_step)):
                # remember that ordered times are backwards if not deque
                # and hence must remove from opposite size as is natural

                # calculate the time that should be removed
                temp_time = old_start_time + index * self.time_step

                # ensure that time to be removed is contained in ordered times
                if temp_time in self.ordered_times:
                    if self.should_use_deque:
                        self.ordered_times.popleft()
                    else:
                        self.ordered_times.pop()
                    self.dict.pop(temp_time, None)
        else:
            # if start time decreased then we must add needed quadtrees
            for index in range(1, round((old_start_time - self.start_time)/self.time_step) + 1):
                # remember that ordered times are backwards if not deque
                # and hence must add from opposite size as is natural

                # calculate the time that should be added
                temp_time = old_start_time - index * self.time_step

                # ensure that time has not already been added to model
                if temp_time not in self.ordered_times:
                    if self.should_use_deque:
                        self.ordered_times.appendleft(temp_time)
                    else:
                        self.ordered_times.append(temp_time)
                    # set dictionary time as well to maintain dictionary
                    self.dict[temp_time] = new_quad_tree_node(temp_time)

    # change end time of model creating quadtree nodes if it is after current end, and deleting quadtree nodes if
    # it is before current end
    def change_end_time(self, new_end_time, new_quad_tree_node):
        # store old end time
        old_end_time = self.end_time
        if new_end_time < self.start_time:
            print("error end time is smaller than start time")
            return

        # calculate difference between end time and start time
        diff = new_end_time - self.start_time

        # calculate new difference going towards larger end time, if not already multiple of difference
        if diff % self.time_step == 0:
            self.end_time = new_end_time
        else:
            # recalculate difference
            diff = (((diff // self.time_step) + 1) * self.time_step)
            # calculate new end time from difference
            self.end_time = self.start_time + diff

        # if end time time has decreased then we must remove unnecessary quadtrees
        if self.end_time < old_end_time:
            # loop through times that are needed to have a quadtree removed
            for index in range(0, round((old_end_time - self.end_time)/self.time_step) + 1):
                # remember that ordered times are backwards if not deque
                # and hence must remove from opposite size as is natural

                # calculate the time that should be removed
                temp_time = old_end_time - index * self.time_step

                # ensure that time to be removed is contained in ordered times
                if temp_time in self.ordered_times:
                    if self.should_use_deque:
                        self.ordered_times.pop()
                    else:
                        self.ordered_times.pop(0)
                    self.dict.pop(temp_time, None)
        else:
            # if end time increased then we must add needed quadtrees
            # loop through times that are needed to have a quadtree added
            for index in range(0, round((self.end_time - old_end_time)/self.time_step)):
                # remember that ordered times are backwards if not deque
                # and hence must add from opposite size as is natural

                # calculate the time that should be added
                temp_time = old_end_time + index * self.time_step

                # ensure that time has not already been added to model
                if temp_time not in self.ordered_times:
                    if self.should_use_deque:
                        self.ordered_times.append(temp_time)
                    else:
                        self.ordered_times.insert(0, temp_time)
                    # set dictionary time as well to maintain dictionary
                    self.dict[temp_time] = new_quad_tree_node(temp_time)
