class ProductService:
    """商品相关接口"""
    
    def __init__(self,client):
        self.client = client
        
    def list(self,limit=10,skip=0):
        return self.client.get("/product",params={"limit":limit,"skip":skip})
    
    def get(self,product_id):
        return self.client.get(f"/product/{product_id}")
    
    def create(self,title,price):
        return self.client.post("/product",json={"title":title,"price":price})
    
    
    