def product_list() -> list:
    list = [
        "Electric Buffet Warmer",
        "Electric Deep Fryer",
        "Electric Hotplate",
        "Electric Infrared Ceramic Cooker",
        "Electric Chopper",
        "Electric Barbecue Grill"
    ]
    return list

def model_list(product: str) -> list:
    if product == "Electric Buffet Warmer":
        list = ["HD9002A", "HD9002B", "HD9002C", "HD9003A", "HD9003B", "HD9003C", "HD9005", "HD9003G", "HD-BS01"]
    elif product == "Electric Deep Fryer":
        list = ["HD3301_HD3301A", "HD3302_HD3302A", "HD3401_HD3401A", "HD3402_HD3402A", "HD3501_HD3501A"]
    elif product == "Electric Hotplate":
        list = ["HD1001A_HD1011A", "HD2002A_HD2012A", "HD1001B_HD1011B", "HD1012B_HD1012BN", "HD1015B_HD1015BN", "HD1016B",
                "HD03H", "HD2011B_HD2011BN", "HD2012B_HD2012BB", "HD2013B_HD2013BN", "HD2015B_HD2015BN", "HD2016B", "HD02H1"]
    elif product == "Electric Infrared Ceramic Cooker":
        list = ["HD6101A", "HD6201A", "HD6106A", "HD6206A", "HD6103D", "HD6105A", "HD6202B", "HD6202C", "HDCC01", "HDCC06", "HD05", "HD07"]
    elif product == "Electric Chopper":
        list = ["HD-EC01", "HD-EC02"]
    elif product == "Electric Barbecue Grill":
        list = ["HD8001_HD8001C"]
    return list