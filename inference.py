import sys

sys.path.append("waveglow/")

import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wf
import torch

from hparams import create_hparams
from text import text_to_sequence
from train import load_model
from waveglow.glow import WaveGlow


def plot_data(data, figsize=(16, 4)):
    fig, axes = plt.subplots(1, len(data), figsize=figsize)
    for i in range(len(data)):
        axes[i].imshow(data[i], aspect='auto',
                       origin='lower', interpolation='none')

    plt.savefig("Attention_plot.png")


def load_tacotron_model(checkpoint_path, hparams):
    model = load_model(hparams)
    model.load_state_dict(torch.load(checkpoint_path)['state_dict'])
    # model.load_state_dict(torch.load(checkpoint_path))
    _ = model.cuda().eval().half()
    return model


def get_config():
    return {
        "n_mel_channels": 80,
        "n_flows": 12,
        "n_group": 8,
        "n_early_every": 4,
        "n_early_size": 2,
        "WN_config": {
            "n_layers": 8,
            "n_channels": 256,
            "kernel_size": 3
        }
    }


def load_waveglow_model(checkpoint_path):
    waveglow_config = get_config()
    waveglow = WaveGlow(**waveglow_config).cuda()
    checkpoint = torch.load(checkpoint_path)
    model_for_loading = checkpoint['model']
    waveglow.load_state_dict(model_for_loading.state_dict())
    # checkpoint = torch.load(checkpoint_path)
    # waveglow.load_state_dict(checkpoint)
    _ = waveglow.eval().half()
    for k in waveglow.convinv:
        k.float()
    return waveglow


def decode_and_plot(model, sequence):
    mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)
    plot_data((mel_outputs.float().data.cpu().numpy()[0],
               mel_outputs_postnet.float().data.cpu().numpy()[0],
               alignments.float().data.cpu().numpy()[0].T))
    return mel_outputs_postnet


def generate_and_save_audio(waveglow, mel_outputs_postnet, hparams):
    with torch.no_grad():
        audio = waveglow.infer(mel_outputs_postnet, sigma=0.666)
        aud = audio[0].data.cpu().numpy()
    wf.write('generated_audio.wav',
             hparams.sampling_rate, aud.astype('float32'))


def get_hparams():
    hparams = create_hparams()
    hparams.sampling_rate = 22050
    return hparams


def main():
    text = "काठमाडौं महानगरपालिकाका नवनिर्वाचित मेयर वालेन्द्र साहलाई बधाई दिनेको ओइरो लागेको छ"
    # text = "nvnirvaacit meyr saahle sthaaniiy thmaa aaphno jitlaaii vijy nbher kaamko suruvaatko rupmaa lieko btaaekaa chn"
    sequence = np.array(text_to_sequence(text, ['basic_cleaners']))[None, :]
    sequence = torch.autograd.Variable(
        torch.from_numpy(sequence)).cuda().long()

    # get hparams
    print("===LOADING HYPERPARAMETERS===")
    hparams = get_hparams()

    # tacotron checkpoint path
    tacotron_checkpoint_path = "output/checkpoint_34000"
    waveglow_checkpoint_path = "output/waveglow_50000"

    # tacotron_checkpoint_path = "output/pretrained_model.pt"
    # waveglow_checkpoint_path = "output/waveglow_256channels_universal_v5.pt"

    # load models
    print("======LOADING MODELS========")
    model = load_tacotron_model(tacotron_checkpoint_path, hparams)
    waveglow = load_waveglow_model(waveglow_checkpoint_path)
    print("====MODELS LOADED SUCCESSFULLY====")

    # generate outputs
    print("====GENERATING ATTENTION WEIGHTS====")
    mel_outputs_postnet = decode_and_plot(model, sequence)

    # generate audio and save it
    print("=====GENERATING AUDIO=====")
    generate_and_save_audio(waveglow, mel_outputs_postnet, hparams)
    print("====AUDIO SAVED====")


if __name__ == "__main__":
    main()
