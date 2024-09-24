
# Create the plots for each ensemble
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

for idx, ensemble in enumerate(['ER', 'KSEQ']):
    # Get the data for the current ensemble
    ensemble_data = Value_df.xs(ensemble, level='Ensemble')
    
    # Plot the data points for each realization
    for repetition in ensemble_data.index:
        axes[idx].scatter(metrics, ensemble_data.loc[repetition], color='k', alpha=0.6, label=f'{ensemble} realizations' if repetition == 0 else "")

    # Overlay the empirical values
    axes[idx].plot(metrics, [Motifs_empirical[motif] for motif in metrics], color='red', marker='o', linestyle='--', label='Empirical values')

    # Set plot labels and title
    axes[idx].set_title(f'{ensemble} Ensemble')
    axes[idx].set_xlabel('Motif Type')
    axes[idx].set_ylabel('Number of Motifs')
    axes[idx].legend()

# Adjust layout and show plot
plt.tight_layout()
plt.show()