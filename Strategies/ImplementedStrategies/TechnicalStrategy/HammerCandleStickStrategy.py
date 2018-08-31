from Signals.Signals import signal_is_volume_high_enough, signal_hammer
from Strategies.Abstract_Strategy import Abstract_Strategy
from Utils.StockDataUtils import calculate_stopbuy_and_stoploss


class HammerCandleStickStrategy (Abstract_Strategy):

    def run_strategy(self):
        #TODO parameter
        raise NotImplementedError('TODO')

    def strat_candlestick_hammer_hi_vol(stock_name, stock_data, hammer_length_in_factor,
                                        handle_bigger_than_head_factor):
        if stock_name is None or stock_data is None or hammer_length_in_factor is None or handle_bigger_than_head_factor is None:
            raise NotImplementedError

        if not signal_is_volume_high_enough(stock_data):
            return {'buy': False}

        if not signal_hammer(stock_data, hammer_length_in_factor, handle_bigger_than_head_factor):
            return {'buy': False}

        result = calculate_stopbuy_and_stoploss(stock_data)

        return {'buy': True, 'get_stock_name': stock_name, 'sb': result['sb'], 'sl': result['sl'],
                'strategy_name': get_current_function_name()}

