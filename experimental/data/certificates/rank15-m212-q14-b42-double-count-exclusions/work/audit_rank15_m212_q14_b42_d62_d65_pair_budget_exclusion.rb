#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"

ROOT = File.expand_path("..", __dir__)
PINS = {
  "work/RANK15_M212_Q14_B42_D62_D65_PAIR_BUDGET_EXCLUSION.md" =>
    "9ad321eb5bb707180bc1d881583fbd867ba4ebcf2b53398054bf207069319ffc",
  "work/verify_rank15_m212_q14_b42_d62_d65_pair_budget_exclusion.py" =>
    "5472091652723f840452a7d44668b2b201bd0422cb7bb9efd3f4a1348cdded9f"
}.freeze

def check(value, message)
  raise message unless value
end

PINS.each do |relative, expected|
  check(Digest::SHA256.file(File.join(ROOT, relative)).hexdigest == expected,
        "pin drift #{relative}")
end

def enumerate_profiles(double_count)
  target = double_count-3
  square_target = 471-double_count
  number_cap = 211-double_count
  rows = []
  counts = Array.new(13,0)
  walk = nil
  walk = lambda do |weight,total,square,number|
    if weight == 13
      rows << counts[1,12].dup if total == target &&
                                      square == square_target && number <= number_cap
      next
    end
    maximum = [(target-total)/weight,
               (square_target-square)/(weight*weight),number_cap-number].min
    (0..maximum).each do |multiplicity|
      counts[weight] = multiplicity
      walk.call(weight+1,total+weight*multiplicity,
                square+weight*weight*multiplicity,number+multiplicity)
    end
    counts[weight] = 0
  end
  walk.call(1,0,0,0)
  rows
end

def minimal_patterns(threshold)
  rows = []
  counts = Array.new(10,0)
  visit = nil
  visit = lambda do |weight,total|
    if weight == 11
      used = (1..10).select { |w| counts[w-1].positive? }
      rows << counts.dup if !used.empty? && total >= threshold && total-used.min < threshold
      next
    end
    maximum = (threshold+9-total)/weight
    if maximum >= 0
      (0..maximum).each do |multiplicity|
        counts[weight-1] = multiplicity
        visit.call(weight+1,total+weight*multiplicity)
      end
    end
    counts[weight-1] = 0
  end
  visit.call(1,0)
  rows
end

groups = (1..10).to_h { |threshold| [threshold,minimal_patterns(threshold)] }
memo = {}
cover = nil
cover = lambda do |state,threshold|
  key = [state,threshold]
  next memo[key] if memo.key?(key)
  best = 0
  groups.fetch(threshold).each do |group|
    next unless (0...10).all? { |index| group[index] <= state[index] }
    rest = (0...10).map { |index| state[index]-group[index] }
    best = [best,1+cover.call(rest,threshold)].max
  end
  memo[key] = best
end

profile_counts = {}
packing_counts = {}
ledger = {}
terminal_counts = {}
(62..65).each do |double_count|
  profiles = enumerate_profiles(double_count)
  profile_counts[double_count] = profiles.length
  kept = profiles.select do |profile|
    small = profile[0,10]
    big = profile[10]+profile[11]
    small.each_with_index.all? do |multiplicity,index|
      next true if multiplicity.zero?
      rest = small.dup
      rest[index] -= 1
      index+4 <= big+cover.call(rest,10-index)
    end
  end
  packing_counts[double_count] = kept.length

  negative = 0
  pair_rejects = 0
  minimum_gap = nil
  terminals = []
  kept.each do |profile|
    multiplicities = []
    profile.each_with_index do |count,index|
      count.times { multiplicities << index+4 }
    end
    heavy = multiplicities.select { |k| k >= 11 }
    h = heavy.length
    z_max = 42-heavy.inject(0,:+)+h*(h-1)/2
    if z_max < 0
      negative += 1
      next
    end
    demand = multiplicities.reject { |k| k >= 11 }.inject(0) do |total,k|
      required = [k-h,0].max
      total+required*(required-1)/2
    end
    capacity = z_max*(z_max-1)/2
    gap = demand-capacity
    if gap > 0
      pair_rejects += 1
      minimum_gap = gap if minimum_gap.nil? || gap < minimum_gap
    else
      terminals << multiplicities.sort.reverse
    end
  end
  ledger[double_count] = [negative,pair_rejects,minimum_gap]
  terminal_counts[double_count] = terminals.length

  if double_count == 65
    check(terminals.length == 13, "D65 terminal count")
    terminals.each do |values|
      selected = 0
      incidence = 0
      violated = false
      values.each do |multiplicity|
        selected += 1
        incidence += multiplicity
        quotient,remainder = incidence.divmod(42)
        demand = (42-remainder)*quotient*(quotient-1)/2 +
                 remainder*quotient*(quotient+1)/2
        capacity = selected*(selected-1)/2
        if demand > capacity
          violated = true
          break
        end
      end
      check(violated, "unpaid D65 terminal profile")
    end
  else
    check(terminals.empty?, "unpaid D#{double_count} profile")
  end
end

check(profile_counts == {62=>1825,63=>2172,64=>2573,65=>3103}, "profile counts")
check(packing_counts == {62=>26,63=>41,64=>51,65=>138}, "packing counts")
check(ledger == {
  62=>[10,16,4],63=>[12,29,3],64=>[17,34,2],65=>[49,76,1]
}, "payment ledger")
check(terminal_counts == {62=>0,63=>0,64=>0,65=>13}, "terminal counts")

vector = [profile_counts,packing_counts,ledger,terminal_counts].join(":") + "\n"
output = [
  "AUDIT_RANK15_M212_Q14_B42_D62_D65_PAIR_BUDGET_EXCLUSION: PASS",
  "profile_counts=62:1825,63:2172,64:2573,65:3103 independent=true",
  "packing_survivors=62:26,63:41,64:51,65:138",
  "negative_zmax=62:10,63:12,64:17,65:49",
  "pair_budget=62:16,63:29,64:34,65:76",
  "minimum_gaps=62:4,63:3,64:2,65:1",
  "terminal_profiles=62:0,63:0,64:0,65:13",
  "terminal_subset_pair_rejects=65:13",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector)}",
  "payment=D62-D65",
  "next=D66"
].join("\n") + "\n"

expected_path = File.join(__dir__,
  "audit_rank15_m212_q14_b42_d62_d65_pair_budget_exclusion.expected.txt")
check(File.file?(expected_path), "missing expected output")
check(output == File.binread(expected_path), "expected-output drift")
print output
