import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib import cm
from operator import itemgetter
from .math import *

##################################################
## Library of functions that add specific subplots
## to an axis specified by the user
##################################################
## Author: Clayton Seitz
## Copyright: 2021, The Hebb Project
## Email: cwseitz@uchicago.edu
##################################################

"""
Neuron state variables in time
"""

def add_unit_voltage(ax, rnn, unit=0, trial=0):

    """
    Add the voltage trace for a single neuron

    Parameters
    ----------
    ax : object,
        matplotlib axis object
    rnn : object,
        RNN object
    unit : int, optional
        index of unit to plot
    trial : int, optional
        index of trial to plot
    """

    ax.plot(rnn.I[unit,trial,:], 'k')
    ax.grid(which='both')
    ax.set_ylabel('$\mathbf{PSP} \; [\mathrm{mV}]$')

def add_unit_current(ax, rnn, unit=0, trial=0):

    """
    Add the current trace for a single neuron

    Parameters
    ----------
    ax : object,
        matplotlib axis object
    rnn : object,
        RNN object
    unit : int, optional
        index of unit to plot
    trial : int, optional
        index of trial to plot
    """

    ax.plot(rnn.V[unit,trial,:], 'k')
    xmin, xmax = 0, rnn.nsteps
    ax.hlines(rnn.thr, xmin, xmax, color='red')
    ax.hlines(0, xmin, xmax, color='blue')
    ax.grid(which='both')
    ax.set_ylabel('$\mathbf{V}\; [\mathrm{mV}]$')

def add_unit_spikes(ax, rnn, unit=0, trial=0):

    """
    Add the spikes of a single neuron

    Parameters
    ----------
    ax : object,
        matplotlib axis object
    rnn : object,
        RNN object
    unit : int, optional
        index of unit to plot
    trial : int, optional
        index of trial to plot
    """

    ax.plot(rnn.Z[unit,trial,:], 'k')
    ax.grid(which='both')
    ax.set_ylabel('$\mathbf{Z}(t)$')

def add_unit_refrac(ax, rnn, unit=0, trial=0):

    """
    Add the refractory variable of a single neuron

    Parameters
    ----------
    ax : object,
        matplotlib axis object
    rnn : object,
        RNN object
    unit : int, optional
        index of unit to plot
    trial : int, optional
        index of trial to plot
    """

    ax.plot(rnn.R[unit,trial,rnn.ref_steps:], 'k')
    ax.grid(which='both')
    ax.set_xlabel('t (ms)')
    ax.set_ylabel('$\mathbf{R}(t)$')

def add_raster(ax, spikes, trial=0, n_units=50):

    """
    Generate a raster plot by randomly selecting 'n_units'
    neurons from the tensor 'spikes'.

    **Note : This function does not work well when a small number of units
    of a large population are spiking

    Parameters
    ----------
    ax : object,
        matplotlib axis object
    spikes : ndarray
        tensor of spikes
    focal : int, optional
        index of unit to highlight in red
    trial : int, optional
        index of trial to plot
    n_units : int, optional
        number of units to plot raster, defaults to 50
    """

    units = np.random.choice(spikes.shape[0], n_units, replace=False)
    sub = spikes[units,:,:]
    arr = []
    for unit in units:
        spike_times = np.argwhere(spikes[unit,trial,:] > 0)
        spike_times = spike_times.reshape((spike_times.shape[0],))
        arr.append(spike_times)
        ax.eventplot(arr, colors='black', orientation='horizontal', lineoffsets=1, linelengths=1)

def add_activity(ax, spikes, trial=0, color='red'):

    """
    Plot the population activity (the sum over units at each time step)

    Parameters
    ----------
    ax : object,
        matplotlib axis object
    spikes : ndarray
        tensor of spikes
    trial : int, optional
        index of trial to plot
    color : str, optional
        color for activity plot, defaults to red
    """

    ax.plot(np.sum(spikes[:,trial,:], axis=0), color=color)

"""
Distributions of state variables
"""

def add_input_hist(ax, rnn, unit=0, nbins=20, di=0.02):

    """
    Compute the histogram of current values for a single neuron over
    trials, as a function of time i.e. P(I,t)
    The vector over which P is calculated has shape (1, trials, 1)
    """

    bins = np.linspace(0,1,nbins)
    colors = cm.coolwarm(np.linspace(0,1,rnn.nsteps))
    for t in range(rnn.nsteps):
        vals, bins = np.histogram(rnn.I[unit,:,t], bins=bins)
        vals = vals/(np.sum(vals)*di)
        ax.plot(bins[:-1], vals, color=colors[t])


"""
Visualizing connectivity
"""

def add_kernel_pair(ax1, ax2, N, sigma, q=0.8):

    """
    Draw a pair of connectivity kernels converted to probabilities and
    the product of their probabilities

    Parameters
    ----------
    ax : object,
        matplotlib axis object
    net : object,
        network object
    alpha : float, optional
        transparency param
    """

    x1, y1 = np.sqrt(N)/2, np.sqrt(N)/4
    x2, y2 = np.sqrt(N)/2, 3*np.sqrt(N)/4
    k_ij = torgauss(N, x1, y1, sigma, delta=1)
    k_ji = torgauss(N, x2, y2, sigma, delta=1)
    p_ij, p_ji, p_x = trinomial(k_ij,k_ji,q)
    ax1.imshow(p_ij+p_ji, cmap='coolwarm')
    ax2.imshow(p_ij*p_ji, cmap='coolwarm')

def add_ego_graph(ax, net, alpha=0.5):

    """
    Draw an ego graph by selecting the node with the largest degree and
    drawing it and all of its neighbors

    Parameters
    ----------
    ax : object,
        matplotlib axis object
    net : object,
        network object
    alpha : float, optional
        transparency param
    """

    G = nx.convert_matrix.from_numpy_array(net.C, create_using=nx.DiGraph)
    node_and_degree = G.degree()
    (hub, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]
    inedges = G.in_edges(hub)
    outedges = G.out_edges(hub)
    G = nx.Graph()
    G.add_node(hub)
    for neighbor in inedges:
        G.add_node(neighbor[0])
        G.add_edge(*neighbor, color='red')
    for neighbor in outedges:
        G.add_node(neighbor[1])
        G.add_edge(*neighbor, color='dodgerblue')
    pos = nx.spring_layout(G)
    edges = G.edges()
    colors = [G[u][v]['color'] for u,v in edges]
    nx.draw(G, pos, ax=ax, alpha=alpha, node_color='black', edge_color=colors, node_size=20, with_labels=False)

def add_spectral_graph(ax, net, alpha=0.05, arrows=False):

    """
    Draw a graph in spectral format

    Parameters
    ----------
    ax : object,
        matplotlib axis object
    net : object,
        network object
    alpha : float, optional
        transparency param
    arrows : bool, optional
        whether or not to draw the direction of an edge via arrows
    """

    C = np.zeros_like(net.C)
    C[np.nonzero(net.C)] = 1
    if arrows: arrows = True
    G = nx.convert_matrix.from_numpy_array(C, create_using=nx.DiGraph)
    pos = nx.spectral_layout(G)
    colors = []
    for n in G.nodes():
        colors.append('dodgerblue')
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=20, node_shape='x')
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='black', alpha=alpha, arrows=arrows, arrowsize=10)

def add_spring_graph(ax, net, alpha=0.05, arrows=False):

    """
    Draw a graph in spring format

    Parameters
    ----------
    ax : object,
        matplotlib axis object
    net : object,
        network object
    alpha : float, optional
        transparency param
    arrows : bool, optional
        whether or not to draw the direction of an edge via arrows
    """

    C = np.zeros_like(net.C)
    C[np.nonzero(net.C)] = 1
    if arrows: arrows = True
    G = nx.convert_matrix.from_numpy_array(C, create_using=nx.DiGraph)
    pos = nx.spring_layout(G)
    colors = []
    for n in G.nodes():
        try:
            if n in net.ex_idx:
                colors.append('red')
            else:
                colors.append('dodgerblue')
        except:
            colors.append('red')
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=20, node_shape='x')
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='black', alpha=alpha, arrows=arrows, arrowsize=10)

def add_fractal_graph(ax, net, alpha=0.05):

    """
    Draw a fractal graph

    Parameters
    ----------
    ax : object,
        matplotlib axis object
    net : object,
        network object
    alpha : float, optional
        transparency param
    arrows : bool, optional
        whether or not to draw the direction of an edge via arrows
    """

    def level_mat(mx_lvl, sz_cl):
        level_mat = np.zeros((2**mx_lvl,2**mx_lvl), dtype=np.int8)
        i = 0
        for k in range(sz_cl+1,mx_lvl+1):
            i += 1
            for n in range(2**(mx_lvl-k)):
                level_mat[n*2**k:, :n*2**k] = i
                level_mat[:n*2**k, n*2**k:] = i
        return level_mat

    G = nx.convert_matrix.from_numpy_array(net.C)
    idxs = np.argwhere(net.C > 0)
    level_mat = level_mat(net.mx_lvl, net.sz_cl)

    colors = cm.coolwarm(np.linspace(0,1,net.mx_lvl-net.sz_cl))
    for idx in idxs:
        x,y = idx; color_idx = int(level_mat[x,y])
        G.edges[x,y]['color'] = colors[color_idx]

    colors = [G[u][v]['color'] for u,v in G.edges()]
    pos = nx.spring_layout(G)
    nx.draw(G, pos, ax=ax, alpha=alpha, node_size=5, node_color='black', edge_color=colors)
    plt.tight_layout()

"""
Visualizing statistical models
"""

def add_ou_hist(ax, ou, steps):

    ax.plot(ou._x, ou.p1[:,steps[0]], color='red', linestyle='--',)
    ax.plot(ou._x, ou.p1[:,steps[1]], color='blue', linestyle='--')
    ax.plot(ou._x, ou.p1[:,steps[2]], color='cyan', label='FP - 200ms', linestyle='--')

    ax.plot(ou._x, ou.p2[:,steps[0]], color='red')
    ax.plot(ou._x, ou.p2[:,steps[1]], color='blue')
    ax.plot(ou._x, ou.p2[:,steps[2]], color='cyan', label='Sim - 200ms')

    ax.set_xlim([-1, 1])
    ax.set_xlabel('X', fontsize=14)
    ax.set_ylabel('P(X)', fontsize=14)
    plt.tight_layout()
    plt.legend()
    plt.grid()
