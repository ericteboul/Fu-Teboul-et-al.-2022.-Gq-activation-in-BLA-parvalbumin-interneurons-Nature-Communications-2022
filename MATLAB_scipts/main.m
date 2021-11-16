
% Note this script is dependent on preprocessing with MatWAND! 
user_input.path  ='T:\Eric\NatCommun Revisions\In vivo C57 no virus control\analysis_bla'; 
user_input.freq_range = [70, 120]; %set frequency range (ex: [70, 120])  
user_input.conditions = {'wt_base', 'wt_inj1', 'wt_inj2'}; %set conditions set in MatWAND (ex: {'wt_base', 'wt_inj1', 'wt_inj2'})
user_input.baseline_cond = 1; % set a condition order number to baseline for normalization 
user_input.analyze_cond = 2:3; % set conditions to be analyzed 
user_input.time_selection = [50, 100]; % set time window to be analyzed (in percent). ex: 50-100% = final 30 minutes of a 60 minute recording.  

% when values above are assigned, this script is ready to run!  

edges = -2:0.01:5;

% init object
dist_obj = PowerDist(user_input);

% % get KDE per animal across conditions
kde = dist_obj.get_kde(edges);
%
% % plot aver KDE
figure()
dist_obj.plot_aver_kde(kde, edges)

% select power higher than 1 std
[power, thresholds] = dist_obj.select_power(1);

% run paired t-test
[h,p,ci,stats] = ttest(power(:,1), power(:,2));

% put in prism array
tail_powers = cell(3, length(dist_obj.conditions)+1);
tail_powers(1, 2:end) = dist_obj.conditions;
tail_powers{1,1} = [num2str(user_input.freq_range(1)) ' - ' num2str(user_input.freq_range(2)) ' Hz'];
tail_powers{2,1} = 'Norm. Power';
tail_powers{3,1} = 'Threshold mean + STD';
for i = 1: size(power,2)
    tail_powers{2, i+1} = power(:,i);
    tail_powers{3, i+1} = thresholds(:,i);
end



%%% KS TEST
% % get power
% all_powers = dist_obj.get_power();
%
% % get kstest
% [h_ks,p_ks,ks2stat]  = kstest2(all_powers{1}, all_powers{2});



