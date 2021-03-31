import json


def check(file):
    with open(file, "r") as f:
        data = json.load(f)
        count = 0
        model_type = {}
        for r in data:
            if r["model"] == "restaurant.restaurant":
                count += 1
            if r["model"] not in model_type:
                model_type[r["model"]] = 1
                print(r)
            else:
                model_type[r["model"]] += 1

        print(count)
        print(model_type)


def reduce():
    # Get 1150 restaurants
    rest_count = 0
    yelp_detail_set = set()
    business_id_set = set()
    with open("data.json", "r") as f:
        data = json.load(f)
        for r in data:
            if r["model"] == "restaurant.restaurant":
                if 1000 <= rest_count < 2000:
                    yelp_detail_set.add(r["fields"]["yelp_detail"])
                    business_id_set.add(r["fields"]["business_id"])
                rest_count += 1

    # Append selected data to result
    result = []
    with open("data.json", "r") as f:
        data = json.load(f)
        for r in data:
            model_type = r["model"]
            if model_type == "restaurant.yelprestaurantdetails":
                if r["pk"] in yelp_detail_set:
                    result.append(r)
            elif model_type == "restaurant.restaurant":
                if r["fields"]["business_id"] in business_id_set:
                    result.append(r)
            elif model_type == "restaurant.inspectionrecords":
                if r["fields"]["business_id"] in business_id_set:
                    result.append(r)
            elif model_type != "user.dinesafelyuser":
                result.append(r)

    for r in result:
        if r["model"] == "restaurant.restaurant":
            if r["fields"]["yelp_detail"] not in yelp_detail_set:
                result.remove(r)

    file = open("data_0330.json", "w")
    json.dump(result, file)
    file.close()
    # check("data_0330.json")


if __name__ == "__main__":
    reduce()
