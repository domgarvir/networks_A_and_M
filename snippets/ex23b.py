# Filter the data to only include the ER model -
df_er = Value_df.xs('ER', level='Ensemble')
# Filter the data to only include the CONF model -
df_conf = Value_df.xs('CONF', level='Ensemble')
# Filter the data to only include the KSEQ model -
df_kseq = Value_df.xs('KSEQ', level='Ensemble')

# Plotting the distributions
fig, ax1 = plt.subplots(1, 1, figsize=(12, 5)) #one plot for each quantity

# Plotting Q distribution
ax1.hist(df_er['eta'], bins=10, color='lightgreen', edgecolor='black', alpha=0.6)
ax1.hist(df_conf['eta'], bins=10, color='orange', edgecolor='black', alpha=0.6)
ax1.hist(df_kseq['eta'], bins=100, color='c', edgecolor='black', alpha=0.6)
ax1.axvline(eta_emp, color='k', linestyle='--')
ax1.set_title('Distribution of Nestedness')
ax1.set_xlabel(r'Nestedness($\eta$)')
ax1.set_ylabel('Frequency')
