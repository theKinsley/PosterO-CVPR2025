import torch
import random
import numpy as np
import argparse
import os

def set_seed(seed=42, use_gpu=True, rank=0):
    seed = seed + rank
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if use_gpu:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

def get_args_infer_dataset():
    parser = argparse.ArgumentParser()

    # dataset
    parser.add_argument("--dataset_name", default='pku', type=str, choices=['pku', 'cgl'])
    parser.add_argument("--design_intent_bbox_dir", type=str, required=True)
    parser.add_argument("--annotation_dir", type=str, required=True)
    
    # hyperpm
    parser.add_argument("--exp_name", default='', type=str)
    parser.add_argument("--N", default=1, type=int)

    # divs split model
    # parser.add_argument("--model_divs_ckpt", default='', type=str)

    # large language model
    parser.add_argument("--model_dir", default='', type=str)
    parser.add_argument("--temperature", default=0.7, type=float)
    parser.add_argument("--max_tokens", default=800, type=int)
    parser.add_argument("--top_p", default=1, type=int)
    parser.add_argument("--frequency_penalty", default=0, type=int)
    parser.add_argument("--presence_penalty", default=0, type=int)
    parser.add_argument("--num_return", default=10, type=int)
    parser.add_argument("--stop_token", default="\n\n", type=str)

    # bool
    parser.add_argument("--vis_preview", action='store_true')

    args = parser.parse_args()
    
    if args.dataset_name == 'pku':
        label_info = {
            1: {'type': 'text', 'color': 'green'}, 
            2: {'type': 'logo', 'color': 'red'},
            3: {'type': 'underlay', 'color': 'orange'}
        }
    elif args.dataset_name == 'cgl':
        label_info = {
            1: {'type': 'logo', 'color': 'red'},
            2: {'type': 'text', 'color': 'green'},
            3: {'type': 'underlay', 'color': 'orange'},
            4: {'type': 'embellishment', 'color': 'blue'}
        }
        
    args.dataset_info = {
        'dataset_name': args.dataset_name,
        'design_intent_bbox_dir': args.design_intent_bbox_dir,
        'annotation_dir': args.annotation_dir,
        'label_info': label_info
    }
    
    if args.exp_name == '':
        args.exp_name = args.N
    else:
        args.exp_name = f"{args.exp_name}_{args.N}"
    
    save_dir = os.path.join(os.path.split(args.model_dir)[-1], args.dataset_name)
    os.makedirs(save_dir, exist_ok=True)
    args.save_path = os.path.join(save_dir, f"{{}}_{{}}_{args.exp_name}.pt")
    
    return args