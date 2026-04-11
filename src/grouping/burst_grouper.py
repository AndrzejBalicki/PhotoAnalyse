from datetime import timedelta


class BurstGrouper:

    def group(self, files, timestamps):

        if not files:
            return []

        paired = list(zip(files, timestamps))
        paired.sort(key=lambda x: x[1])

        groups = []
        current_group = [paired[0][0]]

        threshold = timedelta(seconds=0.5)

        for i in range(1, len(paired)):

            prev_time = paired[i - 1][1]
            curr_time = paired[i][1]

            if curr_time - prev_time <= threshold:
                current_group.append(paired[i][0])
            else:
                groups.append(current_group)
                current_group = [paired[i][0]]

        groups.append(current_group)

        return groups