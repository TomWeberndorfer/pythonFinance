
class StatusUpdate:

    def __init__(self, cnt_to_reach):
        """
        :param cnt_to_reach: number to show the current status, ex: 1/100 stocks read
        """
        self.max_data_reads = cnt_to_reach
        self.curr_data_reads = 0

    def update_status(self, text_to_print):
        """
        update the read status and print it
        :return:
        """
        self.curr_data_reads += 1
        log_text = text_to_print + " " + str(self.curr_data_reads) + "/" + str(self.max_data_reads) + " done."
        print(log_text)

