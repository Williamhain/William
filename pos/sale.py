# sale.py 
class Sale:
    
    def __init__ (self, sale_id, sale_date, subtotal, gst, pst, total):
        self.sale_id = sale_id
        self.sale_date = sale_date
        self.subtotal = subtotal
        self.gst = gst
        self.pst = pst
        self.total = total 
        self.line_items = []
        self._item_counter = 1

    #comment
    def __eq__(self, other):
        return (self.sale_id == other.sale_id and
            self.sale_date == other.sale_date and
            self.subtotal == other.subtotal and
            self.gst == other.gst and
            self.pst == other.pst and
            self.total == other.total)
    
    #returns the list of sale line items in current sale
    def get_number_sale_line_items(self):
        return len(self.line_items) 
