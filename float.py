import argparse

from models.common import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default='best.pt', help='weights path')
    opt = parser.parse_args()

    # Load pytorch model
    model = torch.load(opt.weights, map_location=torch.device('cpu'))['model']

    for name, parameters in model.named_parameters():
        # print(name,':',parameters.size())
        print(parameters.dtype)
