import pandas as pd
import param as pm
import panel as pn
import hvplot.pandas
import holoviews as hv
import numpy as np


class ReserveRatio(pm.Parameterized):
    reserve_ratio = pm.Number(0.35, bounds=(0.01,1), step=0.01)
    price = pm.Number(100, bounds=(100,1000), step=0.01)
    supply = pm.Number(100, bounds=(100,1000), step=0.01)
    
    def x(self):
        return np.linspace(0,1000, 1000)
    
    def curve(self, x):
        y = (x**((1/self.reserve_ratio)-1) * self.price) / (self.supply**((1/self.reserve_ratio)-1))
        return pd.DataFrame(zip(x,y),columns=['supply','price'])
    
    def view(self):
        curve = self.curve(self.x())
        return curve.hvplot.line(x='supply',y='price', line_width=8)


class Formula(pm.Parameterized):
    initial_balance = pm.Number(1e6, bounds=(1e6,2e6), step=1e3)
    initial_supply = pm.Number(1e6, bounds=(1e6,2e6), step=1e3)
    initial_price = pm.Number(3, bounds=(0.1,10), step=0.1)
    expected_growth = pm.Number(100, bounds=(5,1000), step=5)
    r = pm.Number(0.5, bounds=(0,1), step=0.01)
    
    def expected_price(self):
        expected_price = self.initial_price * np.sqrt(self.expected_growth)
        return expected_price
    
    def expected_marketcap(self):
        return self.initial_price * self.initial_supply * self.expected_growth
    
    def projected_supply(self):
        expected_price = self.expected_price()
        projected_supply = (expected_price / (self.expected_marketcap()**(1-self.r) * self.initial_price**self.r))**(1/(self.r-1))
        return projected_supply
    
    def virtual_supply(self):
        projected_supply = self.projected_supply()
        virtual_supply = projected_supply - self.initial_supply
        return virtual_supply
    
    def projected_balance(self):
        projected_balance = self.initial_price * self.projected_supply() * self.r
        return projected_balance
    
    def virtual_balance(self):
        projected_balance = self.projected_balance()
        virtual_balance = projected_balance - self.initial_balance
        return virtual_balance
    
    def info(self):
        expected_price = self.expected_price()
        data= pd.DataFrame([expected_price, self.expected_marketcap(), 
                             self.projected_balance(), self.projected_supply(),
                             self.virtual_balance(), self.virtual_supply()], index=['Expected Price', 'Expected Marketcap', 'Projected Balance',
                                                                                   'Projected Supply', 'Virtual Balance', 'Virtual Supply'])
        data[0] = data[0].round(decimals=4).astype(str)
        return data
    
    def x(self):
        return np.linspace(0,1e6, 1000)
    
    def curve(self, x):
        y = (x**((1/self.r)-1) * self.initial_balance) / (self.r * self.initial_supply**((1/self.r)-1))
        return pd.DataFrame(zip(x,y),columns=['supply','price'])
    
    def virtual_curve(self, x):
        y = (x**((1/self.r)-1) * (self.initial_balance+self.virtual_balance())) / (self.r * (self.initial_supply+self.virtual_supply())**((1/self.r)-1))
        return pd.DataFrame(zip(x,y),columns=['supply','price'])
    
    def view(self):
        curve = self.curve(self.x())
        virtual_curve = self.virtual_curve(self.x())
        return curve.hvplot.line(x='supply',y='price', line_width=5, label='vanilla') * virtual_curve.hvplot.line(x='supply',y='price', line_width=5, label='virtual')

class Fundraising(pm.Parameterized):
    total_raised = pm.Number(1e6, bounds=(1e5, 1e7), precedence=-1)
    hatch_tribute = pm.Number(0.05, bounds=(0,1), precedence=-1)
    hatch_price = pm.Number(1, bounds=(0.5,2), precedence=-1)
    initial_price = pm.Number(2, bounds=(1,4))
    expected_growth = pm.Number(200, bounds=(1,300))
    reserve_ratio = pm.Number(0.1, bounds=(0,1))
    entry_tribute = pm.Number(0.0, bounds=(0,0.5), precedence=-1)
    exit_tribute = pm.Number(0.0, bounds=(0,0.5), precedence=-1)
    token_supply = pm.Number(0)
    reserve_balance = pm.Number(0)
    
    def xrate(self):
        return 1 / self.hatch_price
    
    def growth(self):
        return self.expected_growth
    
    def pctOffered(self):
        return 1
    
    def pctBeneficiary(self):
        return self.hatch_tribute
    
    def sSupply(self):
        return self.total_raised * self.xrate()
    
    def sBalance(self):
        return self.total_raised * (1 - self.hatch_tribute)
    
    def sPrice(self):
        return self.initial_price
    
    def sMarketCap(self):
        return self.sSupply() * self.sPrice()
    
    def eMarketCap(self):
        return self.sMarketCap() * self.growth()
    
    def ePrice(self):
        return self.sPrice() * np.sqrt(self.growth())
    
    def ppSupply(self):
#         ppSupply = (ePrice / (eMarketCap ** (1 - reserveRatio) * (sPrice ** reserveRatio))) ** (1 / (reserveRatio - 1))
        return (self.ePrice() / (self.eMarketCap()**(self.reserve_ratio - 1) * (self.sPrice() ** self.reserve_ratio))) ** (1 / (self.reserve_ratio - 1))
                                                   
    def vSupply(self):
        return self.ppSupply() - self.sSupply()
    
    def ppBalance(self):
        return self.sPrice() * self.ppSupply() * self.reserve_ratio
    
    def vBalance(self):
        return self.ppBalance() - self.sBalance()
    
    def get_outputs(self):
        outputs = pd.DataFrame({
            "sSupply": self.sSupply(),
            "sBalance": self.sBalance(),
            "sPrice": self.sPrice(),
            "sMarketcap": self.sMarketCap(),
            "ePrice": self.ePrice(),
            "eMarketCap": self.eMarketCap(),
            "ppSupply": self.ppSupply(),
            "vSupply": self.vSupply(),
            "ppBalance": self.ppBalance(),
            "vBalance": self.vBalance(),
        }, index=['Value'])
        return outputs
    
    def view_outputs(self):
        outputs = self.get_outputs()
        return outputs.apply(lambda x: round(x, 2)).T

    def buy_amount(self, supply, collateral, pay_amount, reserve_ratio):
        # buyAmt = tokenSupply * ((1 + amtPaid / collateral)^CW — 1)
        return supply * ((1 + pay_amount / collateral)**reserve_ratio - 1)
    
    def sell_amount(self, supply, collateral, sell_amount, reserve_ratio):
        # sellAmt = collateral * ((1 + tokensSold / totalSupply)^(1/CW) — 1)
        return collateral * ((1 + sell_amount / supply)**(1/reserve_ratio) - 1)
    
    def make_buy_order(self, buy_amount):
        fee = buy_amount * self.entry_tribute
        buy_amount = buy_amount - fee
        self.reserve_balance += buy_amount
        collateral_supply = self.token_supply + self.vSupply()
        collateral_balance = self.reserve_balance + self.vBalance()
        return_amount = self.buy_amount(collateral_supply, collateral_balance, buy_amount, self.reserve_ratio)
        self.token_supply += return_amount
        return return_amount
        
    def make_sell_order(self, sell_amount):
        collateral_supply = self.token_supply + self.vSupply()
        collateral_balance = self.reserve_balance + self.vBalance()
        return_amount = self.sell_amount(collateral_supply, collateral_balance, sell_amount, self.reserve_ratio)
        fee = return_amount * self.exit_tribute 
        self.token_supply -= sell_amount
        self.reserve_balance -= return_amount - fee
        return return_amount - fee    
    
    def get_buy_price(self, token_supply=None, reserve_balance=None, amount_wxdai=1e-6):
        if token_supply is None:
            token_supply = self.token_supply
        if reserve_balance is None:
            reserve_balance = self.reserve_balance
        return amount_wxdai / self.buy_amount(token_supply + self.vSupply(), reserve_balance + self.vBalance(), amount_wxdai, self.reserve_ratio)
    
    def get_sell_price(self, token_supply=None, reserve_balance=None, amount_tec=1e-6):
        if token_supply is None:
            token_supply = self.token_supply
        if reserve_balance is None:
            reserve_balance = self.reserve_balance
        return self.sell_amount(token_supply + self.vSupply(), reserve_balance + self.vBalance(), amount_tec, self.reserve_ratio) / amount_tec
    
    def view_price_supply_chart(self):
        x = np.linspace(0,1e6,1000)
        y = self.get_buy_price(token_supply=x)
        df = pd.DataFrame(zip(x,y),columns=['supply','price'])
        return df.hvplot.area(x='supply',y='price')


def abc_debug_app():

    # Introduction
    introduction = pn.pane.Markdown("""
### The commonsstack commonsbuild presents
    The commons config dashboard. 

    See here for more information:
    https://hackmd.io/HTrPYtZdS1q3uiSg1gFbTw?view
    """)

    # ReserveRatio
    params = {    
        'reserve_ratio':0.35,
        'price':100,
        'supply':100,
    }
    reserve_ratio = ReserveRatio(**params)
    reserve_ratio_view = pn.Row(reserve_ratio, reserve_ratio.view)


    # The Formula
    formula = Formula()
    formula_view = pn.Row(formula, pn.Column(formula.info, formula.view))

    # Fundraising
    fundraising = Fundraising()
    fundraising_view = pn.Row(fundraising, pn.Column(fundraising.view_price_supply_chart, fundraising.view_outputs))

    return [
        introduction,
        reserve_ratio_view,
        formula_view,
        'TEEEEEEEEEEEEEESSSSSSSSSSSSSSSST',
        fundraising_view,
    ]
