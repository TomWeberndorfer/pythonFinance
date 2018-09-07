import Utils.Logger_Instance


class StatusUpdate:

    def __init__(self, cnt_to_reach, status_update=True):
        """
        :param cnt_to_reach: number to show the current status, ex: 1/100 stocks read
        """
        self.max_data_reads = cnt_to_reach
        self.curr_data_reads = 0
        self.status_update = status_update

    def update_status(self, text_to_print):
        """
        update the read status and print it
        :return:
        """

        if self.status_update is True:
            self.curr_data_reads += 1
            log_text = text_to_print + " " + str(self.curr_data_reads) + "/" + str(self.max_data_reads) + " done."
            Utils.Logger_Instance.logger.info("Status_update:" + log_text)
