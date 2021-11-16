classdef PowerDist < dynamicprops
    % get power distribution
    
    properties
        processed_psd_folder = 'processed_psd';
        
        % frequency
        f_idx           % index
        freq            % range
        
        baseline_list
        exp_list
        
    end
    
    methods
        
        function obj = PowerDist(user_input)
            % obj = PowerDist(user_input)
            
            % pass to object
            fn = fieldnames(user_input);
            for k=1:numel(fn)
                % add properties
                addprop(obj, fn{k});
                
                % set the value of these property
                obj.(fn{k}) = user_input.(fn{k});
            end  
            
            % create empty frequency index
            obj.f_idx = [0, 0];
            
            % get psd object
            try
                psd_obj = spectral_analysis_batch.reload_object_path(obj.path);
            catch
                s = load(fullfile(obj.path,'psd_object.mat'));
                psd_obj = s.psd_object;
            end
            
            % get frequency vector
            freq = 0:psd_obj.Fs/psd_obj.winsize:psd_obj.Fs/2;
            obj.freq = freq(psd_obj.F1:psd_obj.F2);
            
            % get frequency index
            obj.f_idx(1) = spectral_analysis_batch.getfreq(psd_obj.Fs, psd_obj.winsize, obj.freq_range(1)) - psd_obj.F1 + 1;
            obj.f_idx(2) = spectral_analysis_batch.getfreq(psd_obj.Fs, psd_obj.winsize, obj.freq_range(2)) - psd_obj.F1 + 1;
            %%% ------------------------------------------------------- %%%
            
            % get experiment list
            file_paths = dir(fullfile(obj.path, obj.processed_psd_folder));
            exp_list = spectral_analysis_batch.get_exp_array(file_paths, obj.conditions, 1);
            
            % refine list and conditions
            obj.baseline_list = exp_list(:, obj.baseline_cond);
            obj.exp_list = exp_list(:, obj.analyze_cond);
            obj.conditions = obj.conditions( obj.analyze_cond);
            
        end
        
        function power_area = get_power_area(obj, loadpath, time_select)
            % power_area = get_power_area(obj, loadpath)
            
            % load power
            load(loadpath, 'proc_matrix')
            
            % get power area for freq range and time
            if time_select == 1
                len = size(proc_matrix,2);
                t_select = round([len*obj.time_selection(1)/100, len*obj.time_selection(2)/100,]);
                if t_select(1) < 1
                    t_select(1) = 1;
                end
                power_area = sum(proc_matrix(obj.f_idx(1):obj.f_idx(2), t_select(1):t_select(2)),1);

            else
                power_area = sum(proc_matrix(obj.f_idx(1):obj.f_idx(2), :),1);
            end
        end
        
        function p_area = get_normalize_power(obj, base_path, condition_path)
            % p_area = get_normalize_power(obj, base_path, condition_path)
            
            % get baseline
            base_power = obj.get_power_area(fullfile(obj.path, obj.processed_psd_folder, base_path), 0);
            baseline_power = mean(base_power);
            
            % power area for each condition normalized by baseline
            p_area  = obj.get_power_area(fullfile(obj.path, obj.processed_psd_folder, condition_path), 1);
            p_area = p_area/baseline_power;

        end
        
        
        function power = get_power(obj) % for ks test
            % power = get_power(obj)
            
            % create wait bar
            w = waitbar(0, 'Please wait...');
            
            cntr = 0;
            power = {};
            for ii = 1:size(obj.exp_list,2)
                
                power_vec = []; % create empty vector
                for i = 1:size(obj.exp_list,1)
                    
                    % get normalized power
                    p_area = obj.get_normalize_power(obj.baseline_list{i}, obj.exp_list{i,ii});
                    
                    % concatenate
                    power_vec = horzcat(power_vec, p_area);
                    
                    % update progress bar
                    waitbar(cntr/numel(obj.exp_list), w, 'Extracting Power...');
                    cntr = cntr+1;
                end
                
                % pass to cell array
                power{ii} = power_vec;
                
            end
            close(w) % close progressbar
        end
      
        function [power, thresholds]  = select_power(obj, threshold) % for t-test
            %  [power, thresholds] = select_power(obj, threshold)
            
            % create wait bar
            w = waitbar(0, 'Please wait...');
            
            cntr = 0;
            power = zeros(size(obj.exp_list)); % create empty vector
            thresholds = zeros(size(obj.exp_list));
            for ii = 1:size(obj.exp_list,2)   % conditions
                for i = 1:size(obj.exp_list,1) % experiments
                    
                    % get normalized power
                    p_area = obj.get_normalize_power(obj.baseline_list{i}, obj.exp_list{i,ii});
                    
                    % filtered
                    threshold_power = (mean(p_area) + threshold*std(p_area));
                    filtered_parea = p_area(p_area > threshold_power);
                    
                    % get power and threshold
                    power(i,ii) = mean(filtered_parea);
                    thresholds(i,ii) = threshold_power; 
                    
                    % update progress bar
                    waitbar(cntr/numel(obj.exp_list), w, 'Extracting Power...');
                    cntr = cntr+1;
                end
                
            end
            close(w) % close progressbar
        end
        
        function kde = get_kde(obj, edges) % for kde plot
            % kde = get_kde(obj, edges)
            
            % get step size
            step_size = mean(diff(edges));
            
            % create wait bar
            w = waitbar(0, 'Please wait...');
            
            cntr = 0;
            kde = {};
            for ii = 1:size(obj.exp_list,2)
                
                % create array to store individual densities
                kde_array = cell(size(obj.exp_list,1),1);
                
                for i = 1:size(obj.exp_list,1)
                    
                    % get normalized power
                    p_area = obj.get_normalize_power(obj.baseline_list{i}, obj.exp_list{i,ii});
                    
                    % get probability density
                    [kde_array{i}, ~] = ksdensity(p_area, edges);
                    
                    % update progress bar
                    waitbar(cntr/numel(obj.exp_list), w, 'Extracting Power...');
                    cntr = cntr+1;
                end
                
                % convert to matrix
                kde_array = vertcat(kde_array{:});
                
                % pass to cell array
                kde{ii} = kde_array*step_size;
                
            end
            close(w) % close progressbar
        end
        
        function plot_aver_kde(obj, kde, edges)
            % plot_aver_kde(obj, kde)
            
            for i = 1:length(kde)
                
                % get mean and fill SEM
                [mean_wave, xfill, yfill] = spectral_analysis_batch.getmatrix_mean(kde{i}', edges);
                
                % plot
                hold on;
                [col_mean, col_sem] = spectral_analysis_batch.color_vec(i+1);
                fill(xfill, yfill, col_sem,'LineStyle','none');
                p(i) = plot(edges, mean_wave,'color', col_mean,'Linewidth',1.5);
                
            end
            
            % add legend, labels, title
            legend(p, strrep(obj.conditions,'_', ' '))
            ylabel('Relative Probability')
            xlabel('Norm. Power')
            title( [num2str(obj.freq_range(1)) ' - ' num2str(obj.freq_range(2)) 'Hz'])
            spectral_analysis_batch.prettify_o(gca)
            
        end
        
    end
    
end










