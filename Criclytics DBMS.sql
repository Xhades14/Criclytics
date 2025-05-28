CREATE TABLE `players` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `date_of_birth` date,
  `age` int,
  `nationality` varchar(255),
  `role` varchar(255),
  `batting_style` varchar(255),
  `bowling_style` varchar(255),
  `total_runs` int,
  `50s` int,
  `100s` int,
  `total_wickets` int,
  `5W` int,
  `debut_date` date,
  `last_updated` timestamp
);

CREATE TABLE `teams` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `nation` char,
  `coach` varchar(255),
  `captain_id` int,
  `squad_size` int,
  `founded_year` int,
  `last_updated` timestamp
);

CREATE TABLE `venues` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `city` varchar(255),
  `country` varchar(255),
  `capacity` int,
  `established_year` int,
  `hosts_id` int
);

CREATE TABLE `formats` (
  `format_name` varchar(255) PRIMARY KEY,
  `overs_limit` int
);

CREATE TABLE `series` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `host_country` varchar(255),
  `host_id` int,
  `start_date` date,
  `end_date` date,
  `format_name` int,
  `number_of_matches` int,
  `winner_id` int,
  `matches_won` int,
  `matches_lost` int,
  `POTT` int,
  `winning_capt` int,
  `sponsor` varchar(255)
);

CREATE TABLE `matches` (
  `id` int PRIMARY KEY,
  `date_of_match` date,
  `venue_id` int,
  `team1_id` int,
  `capt1_id` int,
  `team2_id` int,
  `capt2_id` int,
  `winner_id` int,
  `match_type` varchar(255),
  `series_id` int,
  `format_name` int,
  `toss_winner_id` int,
  `toss_decision` varchar(255),
  `result` varchar(255),
  `POTM` int,
  `winning_capt` int
);

CREATE TABLE `innings` (
  `id` int PRIMARY KEY,
  `match_id` int,
  `team_id` int,
  `inning_number` int,
  `innings_type` varchar(255),
  `runs_scored` int,
  `wickets_lost` int,
  `overs` int
);

CREATE TABLE `player_stats` (
  `inning_id` int,
  `player_id` int,
  `team_id` int,
  `place` varchar(255),
  `runs_scored` int,
  `ball_by_ball_faced` int,
  `fours` int,
  `sixes` int,
  `strike_rate` float,
  `wickets_taken` int,
  `overs_bowled` float,
  `maidens` int,
  `runs_conceded` int,
  `economy` float,
  `catches` int,
  `run_outs` int,
  `stumpings` int,
  PRIMARY KEY (`inning_id`, `player_id`)
);

CREATE TABLE `overs` (
  `id` int PRIMARY KEY,
  `inning_id` int,
  `over_number` int,
  `runs_scored` int,
  `wickets_taken` int,
  `extras` int
);

CREATE TABLE `ball_by_ball` (
  `over_id` int,
  `ball_number` int,
  `batsman_id` int,
  `bowler_id` int,
  `runs_scored` int,
  `is_wicket` boolean,
  `dismissal_type` varchar(255),
  `fielder_id` int,
  `is_boundary` boolean,
  `boundary_type` varchar(255),
  `is_overthrow` boolean,
  `overthrow_runs` int,
  `extra_type` varchar(255),
  `extra_runs` int,
  PRIMARY KEY (`over_id`, `ball_number`)
);

CREATE TABLE `umpires` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `nationality` varchar(255)
);

CREATE TABLE `match_umpires` (
  `match_id` int,
  `umpire_id` int,
  `role` varchar(255),
  PRIMARY KEY (`match_id`, `umpire_id`)
);

CREATE TABLE `player_teams` (
  `player_id` int,
  `team_id` int,
  `from_date` date,
  `to_date` date,
  PRIMARY KEY (`player_id`, `team_id`)
);

ALTER TABLE `player_teams` ADD FOREIGN KEY (`player_id`) REFERENCES `players` (`id`);

ALTER TABLE `player_teams` ADD FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`);

ALTER TABLE `teams` ADD FOREIGN KEY (`captain_id`) REFERENCES `players` (`id`);

ALTER TABLE `player_stats` ADD FOREIGN KEY (`player_id`) REFERENCES `players` (`id`);

ALTER TABLE `player_stats` ADD FOREIGN KEY (`inning_id`) REFERENCES `innings` (`id`);

ALTER TABLE `player_stats` ADD FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`);

ALTER TABLE `matches` ADD FOREIGN KEY (`team1_id`) REFERENCES `teams` (`id`);

ALTER TABLE `matches` ADD FOREIGN KEY (`capt1_id`) REFERENCES `players` (`id`);

ALTER TABLE `matches` ADD FOREIGN KEY (`team2_id`) REFERENCES `teams` (`id`);

ALTER TABLE `matches` ADD FOREIGN KEY (`capt2_id`) REFERENCES `players` (`id`);

ALTER TABLE `matches` ADD FOREIGN KEY (`winner_id`) REFERENCES `teams` (`id`);

ALTER TABLE `matches` ADD FOREIGN KEY (`venue_id`) REFERENCES `venues` (`id`);

ALTER TABLE `matches` ADD FOREIGN KEY (`format_name`) REFERENCES `formats` (`format_name`);

ALTER TABLE `matches` ADD FOREIGN KEY (`series_id`) REFERENCES `series` (`id`);

ALTER TABLE `matches` ADD FOREIGN KEY (`toss_winner_id`) REFERENCES `teams` (`id`);

ALTER TABLE `matches` ADD FOREIGN KEY (`POTM`) REFERENCES `players` (`id`);

ALTER TABLE `matches` ADD FOREIGN KEY (`winning_capt`) REFERENCES `players` (`id`);

ALTER TABLE `innings` ADD FOREIGN KEY (`match_id`) REFERENCES `matches` (`id`);

ALTER TABLE `innings` ADD FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`);

ALTER TABLE `overs` ADD FOREIGN KEY (`inning_id`) REFERENCES `innings` (`id`);

ALTER TABLE `ball_by_ball` ADD FOREIGN KEY (`over_id`) REFERENCES `overs` (`id`);

ALTER TABLE `ball_by_ball` ADD FOREIGN KEY (`batsman_id`) REFERENCES `players` (`id`);

ALTER TABLE `ball_by_ball` ADD FOREIGN KEY (`bowler_id`) REFERENCES `players` (`id`);

ALTER TABLE `ball_by_ball` ADD FOREIGN KEY (`fielder_id`) REFERENCES `players` (`id`);

ALTER TABLE `match_umpires` ADD FOREIGN KEY (`match_id`) REFERENCES `matches` (`id`);

ALTER TABLE `match_umpires` ADD FOREIGN KEY (`umpire_id`) REFERENCES `umpires` (`id`);

ALTER TABLE `venues` ADD FOREIGN KEY (`hosts_id`) REFERENCES `teams` (`id`);

ALTER TABLE `series` ADD FOREIGN KEY (`format_name`) REFERENCES `formats` (`format_name`);

ALTER TABLE `series` ADD FOREIGN KEY (`host_country`) REFERENCES `players` (`nationality`);

ALTER TABLE `series` ADD FOREIGN KEY (`host_id`) REFERENCES `teams` (`id`);

ALTER TABLE `series` ADD FOREIGN KEY (`winner_id`) REFERENCES `teams` (`id`);

ALTER TABLE `series` ADD FOREIGN KEY (`POTT`) REFERENCES `players` (`id`);

ALTER TABLE `series` ADD FOREIGN KEY (`winning_capt`) REFERENCES `players` (`id`);

ALTER TABLE `series` ADD FOREIGN KEY (`host_country`) REFERENCES `teams` (`nation`);
