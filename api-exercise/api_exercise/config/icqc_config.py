class icqc_config:
    mean = [0.5834, 0.5871, 0.5687]
    std = [0.1991, 0.2024, 0.2133]
    height = 224
    width = 336
    num_classes = 4
    stoi = {'blur': 0, 'missing': 1, 'overexposed': 2, 'sharp': 3}
    itos = {0: 'blur', 1: 'missing', 2: 'overexposed', 3: 'sharp'}
    target_names = ['blur', 'missing', 'overexposed', 'sharp']
