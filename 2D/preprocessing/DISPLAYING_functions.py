## 3d visualization import
%gui qt
from mayavi import mlab
mlab.init_notebook('png')


def plot_2d(sample_array, contour = False, clear = True, edges = np.array([])):
    if clear:
        mlab.clf()
    #print(sample_array)
    m = np.max(np.abs(sample_array))
    print(m, len(sample_array.shape))
    s = np.abs(sample_array)
    mlab.figure(figure=None, bgcolor=(0.99,0.99,0.99), fgcolor=None, engine=None, size=(400, 350))
    
    if len(sample_array.shape)==3:
        
        sample_array = np.concatenate((sample_array, sample_array), axis=2)
        
    sample_array = np.abs(sample_array)

    try:
        sample_array = sample_array/m
    except: ## if m is zero
        pass
    n = np.max(np.abs(sample_array))
    print(n)

    sample_array[0,:,:] += 1.2
    sample_array[:,0,:] += 1.2
    sample_array[-1,:,:] += 1.2
    sample_array[:,-1,:] += 1.2
    
    if edges.size > 0:
        sample_array = sample_array + 0.25*edges
        
    volume = mlab.pipeline.volume(mlab.pipeline.scalar_field(sample_array), vmin=0.2, vmax=0.8)
    if contour:
        mlab.contour3d(s)
    
        
    return volume
    
%matplotlib inline 
import matplotlib.pyplot as plt

def plot_grid_2d(concat_input, concat_output):
    
    f, axarr = plt.subplots(2,5, figsize = (15,6)) 
    
    axarr[0,0].imshow(np.abs(concat_input[:,:,0]))
    axarr[0,0].set(title='smoothed map')

    axarr[0,1].imshow(np.abs(concat_input[:,:,1]))
    axarr[0,1].set(title='X displacement B.C.')

    axarr[0,2].imshow(np.abs(concat_input[:,:,2]))
    axarr[0,2].set(title='Y displacement B.C.')

    axarr[0,3].imshow(np.abs(concat_input[:,:,3]))
    axarr[0,3].set(title='Z displacement  B.C')

    axarr[0,4].imshow(np.abs(concat_input[:,:,4]))
    axarr[0,4].set(title='X force B.C.')

    axarr[1,0].imshow(np.abs(concat_input[:,:,5]))
    axarr[1,0].set(title='Y force B.C.')

    axarr[1,1].imshow(np.abs(concat_input[:,:,6]))
    axarr[1,1].set(title='Z force B.C.')

    axarr[1,2].imshow(np.abs(concat_output[:,:,1]))
    axarr[1,2].set(title='X displacement result')

    axarr[1,3].imshow(np.abs(concat_output[:,:,2]))
    axarr[1,3].set(title='Y displacement result')

    axarr[1,4].imshow(np.abs(concat_output[:,:,3]))
    axarr[1,4].set(title='Z displacement result')

    print(sample_number)
    plt.show()
    
print('displaying functions imported. magics imported: <%matplotlib inline>  <%gui qt>')