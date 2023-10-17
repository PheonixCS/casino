<?php 
/*********************************************************/
/**  © 2023 NULLcode Studio. All Rights Reserved.
/**  Разработано в рамках проекта: https://null-code.ru/
/*********************************************************/
class SlotSchemeData
{
	public $width = 0;
	public $height = 0;
	public $slots = array();
	public $lines = array();
	public $bets = array();
	public $preset = array();
	public $freeSpins = array();
	public $complex = array();
	
	function __construct($json) 
	{
		$this->width = intval($json->width);
		$this->height = intval($json->height);
		
		$this->slots = array();
		for ($i = 0; $i < count($json->slots); $i++) {
			$block = new SlotSchemeBlock();
			$block->name = $json->slots[$i]->name;
        	$block->type = $json->slots[$i]->type;
        	$block->percent = intval($json->slots[$i]->percent);
        	$block->id = intval($json->slots[$i]->id);
        	$block->complex = boolval($json->slots[$i]->complex);
        	$block->paytable = array();
        	for ($j = 0; $j < count($json->slots[$i]->paytable); $j++) {
				$blockPrice = new SlotSchemeBlockPrice();
				$blockPrice->count = intval($json->slots[$i]->paytable[$j]->count);
	        	$blockPrice->price = floatval($json->slots[$i]->paytable[$j]->price);
	        	array_push($block->paytable, $blockPrice);
        	}
        	array_push($this->slots, $block);
        }
        
        $this->lines = array();
		for ($i = 0; $i < count($json->lines); $i++) {
			$line = new SlotSchemeLine();
        	$line->data = array();
        	for ($j = 0; $j < count($json->lines[$i]->data); $j++) {
	        	array_push($line->data, intval($json->lines[$i]->data[$j]));
        	}
        	array_push($this->lines, $line);
        }
        
        $this->bets = array();
		for ($i = 0; $i < count($json->bets); $i++) {
			array_push($this->bets, floatval($json->bets[$i]));
        }
        
        $this->preset = array();
		for ($i = 0; $i < count($json->preset); $i++) {
			array_push($this->preset, intval($json->preset[$i]));
        }
        
        $this->freeSpins = array();
		for ($i = 0; $i < count($json->freeSpins); $i++) {
			$free = new SlotSchemeFreeSpins();
        	$free->count = intval($json->freeSpins[$i]->count);
        	$free->price = intval($json->freeSpins[$i]->price);
        	array_push($this->freeSpins, $free);
        }
        
        $this->complex = array();
		for ($i = 0; $i < count($json->complex); $i++) {
			$complex = new SlotSchemeComplex();
			$complex->count = intval($json->complex[$i]->count);
			$complex->price = floatval($json->complex[$i]->price);
			$complex->lineOnly = boolval($json->complex[$i]->lineOnly);
        	array_push($this->complex, $complex);
        }
	}
}

class SlotSchemeBlock
{
	public $name = "";
	public $type = "";
	public $percent = 0;
	public $id = 0;
	public $paytable = array();
	public $complex = false;
}

class SlotSchemeBlockPrice
{
	public $count = 0;
	public $price = 0.0;
}

class SlotSchemeComplex
{
	public $lineOnly =  false;
	public $count = 0;
	public $price = 0.0;
}

class SlotSchemeFreeSpins
{
	public $count = 0;
	public $price = 0;
}

class SlotSchemeLine
{
	public $data = array();
}

class WildSlot
{
	public $data = array();
}

class SpecialCounter
{
	public $type = "";
	public $count = 0;
	public $id = 0;
	
	public function win()
	{
		return $this->count >= 3;
	}
}

class SlotResult
{
	public $balance = 0.0;
	public $totalWin = 0.0;
	public $bet = 0.0;
	public $window = array();
	public $special = array();
	public $lines = array();
	public $complex = array();
	public $freeSpin = false;
	public $bonus = false;
	public $freeSpinCount = 0;
	public $wildID = 0;
	public $bonusName = "";
}

class SlotResultLine
{
	public $win = 0.0;
	public $id = 0;
	public $type = "";
	public $slot = array();
}

class SlotResultLineSlot
{
	public $x = 0;
	public $y = 0;
	public $id = 0;
}

class BlockSpecial
{
	public $type;
	public $counter;
	public $count;
	
	function __construct() 
	{
		$this->type = null;
		$this->counter = null;
		$this->count = 0;
	}
	
	public function isBuild()
	{
		return $this->count >= 3 && $this->type != null;
	}
}

class SlotLogic
{
	public $result;
	public $counters;
	public $isComplex = false;
	public $grid = array();
	public $isSpecial = false;
	public $prev = 0;
	public $count = 0;
	public $list_grid = array();
	public $lineOnly = false;
	
	function __construct() 
	{
		$this->result = null;
		$this->counters = null;
		$this->isComplex = false;
		$this->grid = array();
		$this->isSpecial = false;
		$this->prev = 0;
		$this->count = 0;
		$this->list_grid = array();
		$this->lineOnly = false;
	}	
	
	public function Calculate($scheme, $lines, $bet, $balance, $freeSpinCount, $specialSameTime = false, $complex = false, $wild_ID = -1, $limit = -1, $complex_get = false, $winner = false, $ignoreSpecial = null, $getSpecial = null)
	{
		if ($this->IsLinesError($scheme, $lines) || $this->IsBetError($scheme, $bet))
			return null;
		$this->result = new SlotResult();
		$limit = $this->SetLimit($scheme, $limit, $bet);
		if ($limit == 0)
			$winner = false;
		$this->counters = $this->GetSpecials($scheme);
		$blockSpecial = $this->CheckGetSpecial($scheme, $getSpecial, $ignoreSpecial);
		if ($blockSpecial->isBuild()) {
			$specialSameTime = false;
        	$limit = 0;
        	$complex = false;
        	$ignoreSpecial = array('Bonus', 'FreeSpin');
        }
        if (!$complex) $complex_get = false;
		$wild = $this->GetWild($scheme, $this->CheckWild($scheme, $wild_ID));
		$this->result->bet = count($lines) * $scheme->bets[$bet];
		if ($freeSpinCount == 0)
			$balance -= $this->result->bet;
		$freeSpinCount--;
		if ($freeSpinCount < 0)
			$freeSpinCount = 0;
		$this->result->freeSpinCount = $freeSpinCount;
		while (true) {
			$this->isSpecial = false;
			$this->grid = $this->BuildGrid($scheme, $complex, $blockSpecial);
			if ($complex_get && !$this->isComplex)
				continue;
				if ($this->CheckSpecials($scheme, $ignoreSpecial, $blockSpecial->isBuild() ? null : $blockSpecial->type, $specialSameTime))
				continue;
			$this->result->totalWin = $this->GetWin($scheme, $lines, $bet, $wild);
			if ($this->CheckResult($this->result->totalWin, $winner, $limit == 0, $this->isSpecial))
				continue;
			if ($this->result->totalWin <= $limit || $limit < 0)
				break;
		}
		$this->BuildSpecial($blockSpecial, $scheme);
		$this->result->bonus = $this->FindSpecialType("Bonus", $scheme, $bet);
		$this->result->freeSpin = $this->FindSpecialType("FreeSpin", $scheme, $bet);
		$this->result->lines = $this->SortLines($this->result->lines);
		$this->result->balance = $balance + $this->result->totalWin;
		$this->result->wildID = $wild_ID;
		if ($freeSpinCount > 0)
			$this->result->freeSpin = true;
	}
	
	function IsBetError($scheme, $bet)
	{
		if ($scheme === null || $bet < 0 || $bet > count($scheme->bets) - 1)
			return true;
		return false;
	}

	function IsLinesError($scheme, $lines)
	{
		if ($scheme === null || empty($lines))
			return true;
		for ($i = 0; $i < count($lines); $i++)
			if ($lines[$i] < 0 || $lines[$i] > count($scheme->lines) - 1) return true;
		return false;
	}
	
	function BuildSpecial($block, $scheme)
    {
        if (!$block->isBuild()) return;
        $wheels = array();
        for ($i = 0; $i < $scheme->width; $i++)
            array_push($wheels, $i);
        shuffle($wheels);
        if ($block->counter != null)
        {
            for ($i = 0; $i < $block->count; $i++)
                $this->grid[$wheels[$i]][rand(0, $scheme->height - 1)] = $block->counter->id;
            $this->result->window = array();
            for ($y = 0; $y < $scheme->height; $y++)
				for ($x = 0; $x < $scheme->width; $x++) {
					array_push($this->result->window, $this->grid[$x][$y]);
				}
			for ($i = 0; $i < count($this->counters); $i++) {
				$this->counters[$i]->count = 0;
				for ($y = 0; $y < $scheme->height; $y++)
					for ($x = 0; $x < $scheme->width; $x++) {
					if ($this->grid[$x][$y] == $this->counters[$i]->id)
						$this->counters[$i]->count++;
				}
			}
		}
    }
	
	function IsNullOrEmptyString($str)
	{
    	return ($str === null || trim($str) === '');
	}
	
	function FindSpecialByString($type)
    {
        $special = null;
        for ($i = 0; $i < count($this->counters); $i++) {
        	if ($this->counters[$i]->type == $type) $special = $this->counters[$i];
        }
        return $special;
    }
	
	function CheckGetSpecial($scheme, $str, $ignore)
    {
		$this->result->bonusName = null;
        $blockSpecial = new BlockSpecial();
        if ($this->IsNullOrEmptyString($str)) return $blockSpecial;
        $arr = explode('=', $str);
        if (count($arr) == 1 && !$this->CheckNameSpecial($arr[0]) || count($arr) > 2) return $blockSpecial;
        if (count($arr) == 1 && $this->CheckNameSpecial($arr[0])) {
        	if (empty($ignore)) $blockSpecial->type = $arr[0];
        	return $blockSpecial;
        }
		$part = explode('|', $arr[1]);
		$count = abs($this->int_GetParse($part[0]));
        if (!$this->CheckNameSpecial($arr[0]) || $count > $scheme->width || $count < 3) return $blockSpecial;
        $blockSpecial->type = $arr[0];
        $blockSpecial->counter = $this->FindSpecialByString($arr[0]);
        $blockSpecial->count = $count;
		if ($blockSpecial->counter->type == "FreeSpin" && count($part) == 2) {
			$countFree = abs($this->int_GetParse($part[1]));
			if ($countFree > 0) {
				for ($i = 0; $i < count($scheme->freeSpins); $i++) {
					if ($scheme->freeSpins[$i]->count == $count)
						$scheme->freeSpins[$i]->price = $countFree;
				}
			}
		}
		if ($blockSpecial->counter->type == "Bonus" && count($part) == 2) {
			$this->result->bonusName = $this->IsNullOrEmptyString($part[1]) ? null : $part[1];
		}
        return $blockSpecial;
    }

    function int_GetParse($str)
    {
        $int_value = ctype_digit($str) ? intval($str) : null;
		if ($int_value === null)
			return 0;
		return $int_value;
    }
	
	function CheckNameSpecial($str)
    {
        return $str == "Bonus" || $str == "FreeSpin";
    }
	
	function SortLines($lines)
	{
		if (count($lines) == 0)
			return $lines;
		$clone = array();
		$bonus = $this->SortLinesFind($lines, "Bonus");
		$freeSpin = $this->SortLinesFind($lines, "FreeSpin");
		if ($bonus == null && $freeSpin == null)
			return $lines;
		if ($bonus != null)
			array_push($clone, $bonus);
		if ($freeSpin != null)
			array_push($clone, $freeSpin);
		for ($i = 0; $i < count($lines); $i++) {
			if ($lines[$i]->type == "Chip")
				array_push($clone, $lines[$i]);
		}
		return $clone;
	}
	
	function SortLinesFind($lines, $type)
	{
		for ($i = 0; $i < count($lines); $i++) {
			if ($lines[$i]->type == $type)
				return $lines[$i];
		}
		return null;
	}
	
	function CheckResult($win, $winner, $lose, $special)
	{
		return $win == 0 && !$special && $winner || $win > 0 && $lose || $special && $lose;
	}
	
	function FindSpecialType($type, $scheme, $bet)
	{
		for ($i = 0; $i < count($this->counters); $i++)
			if ($type == $this->counters[$i]->type && $this->counters[$i]->win()) {
			$slot = array();
			for ($y = 0; $y < $scheme->height; $y++)
				for ($x = 0; $x < $scheme->width; $x++) {
				if ($this->grid[$x][$y] == $this->counters[$i]->id) {
					$lineSlot = new SlotResultLineSlot();
					$lineSlot->y = $y;
					$lineSlot->x = $x;
					$lineSlot->id = $this->counters[$i]->id;
					array_push($slot, $lineSlot);
				}
			}
			$resultLine = new SlotResultLine();
			$resultLine->id = -1;
			$resultLine->type = $type;
			$resultLine->win = $this->GetPaytable($scheme, $this->counters[$i]->id, count($slot)) * $scheme->bets[$bet];
			$resultLine->slot = $slot;
			array_push($this->result->lines, $resultLine);
			$this->result->totalWin += $resultLine->win;
			$this->result->freeSpinCount += $this->GetFreeSpins($scheme, $type, count($slot));
			return true;
		}
		return false;
	}
	
	function GetFreeSpins($scheme, $type, $count)
	{
		if ($type != "FreeSpin")
			return 0;
		for ($i = 0; $i < count($scheme->freeSpins); $i++) {
			if ($scheme->freeSpins[$i]->count == $count)
				return $scheme->freeSpins[$i]->price;
		}
		return 0;
	}
	
	function GetWin($scheme, $lines, $bet, $wild)
	{
		$this->result->lines = array();
		$this->result->complex = array();
		$win = 0.0;
		$complexSlot = new SlotResultLineSlot();
		for ($i = 0; $i < count($lines); $i++) {
			$slot = array();
			$line = array();
			for ($y = 0; $y < $scheme->height; $y++) {
				$item = array();
				for ($x = 0; $x < $scheme->width; $x++) {
					$item[] = 0;
				}
				$line[] = $item;
			}
			$j = 0;
			for ($y = 0; $y < $scheme->height; $y++) {
				for ($x = 0; $x < $scheme->width; $x++) {
					$line[$x][$y] = $scheme->lines[$lines[$i]]->data[$j];
					$j++;
				}
			}
			$check_line = true;
			for ($x = 0; $x < $scheme->width; $x++) {
				for ($y = 0; $y < $scheme->height; $y++) {
					if ($line[$x][$y] == 1 && $check_line) {
						if ($this->CheckSlotLine($slot, $this->grid[$x][$y], $wild)) {
							array_push($slot, $this->GetLineSlot($x, $y, $this->grid[$x][$y]));
						} else {
							$check_line = false;
						}
					}

					if ($y + 1 < $scheme->height && $this->grid[$x][$y] == $this->grid[$x][$y + 1]) {
						$complexSlot->y = $y;
						$complexSlot->x = $x;
						$complexSlot->id = $this->grid[$x][$y];
					}
				}
			}
			$value = $this->GetPaytableList($scheme, $slot, $wild) * $scheme->bets[$bet];
			if ($value > 0) {
				$resultLine = new SlotResultLine();
				$resultLine->id = $lines[$i];
				$resultLine->type = "Chip";
				$resultLine->win = $value;
				$resultLine->slot = $slot;
				array_push($this->result->lines, $resultLine);
			}
			$win += $value;
		}
		if ($complexSlot->id > 0) {
			$tmp = array();
			$x = $complexSlot->x;
			for ($y = 0; $y < $scheme->height; $y++) {
				if (count($tmp) == 0 && $this->grid[$x][$y] == $this->grid[$x][$y + 1])
					array_push($tmp, $this->GetLineSlot($x, $y, $this->grid[$x][$y]));
				else if (count($tmp) > 0 && $this->grid[$x][$y] == $tmp[0]->id)
					array_push($tmp, $this->GetLineSlot($x, $y, $this->grid[$x][$y]));
				else if (count($tmp) > 0 && $this->grid[$x][$y] != $tmp[0]->id)
					break;
			}
			$this->result->complex = $tmp;
			$this->lineOnly = false;
			$complexWin = $this->GetComplexWin($scheme, count($this->result->complex));
			if ($this->lineOnly) {
				for ($i = 0; $i < count($this->result->complex); $i++)
					if ($this->FindComplexInLine($this->result->complex[$i]->x, $this->result->complex[$i]->y, $this->result->complex[$i]->id)) {
					$win += $complexWin;
					break;
				}
			} else
				$win += $complexWin;
		}
		return $win;
	}
	
	function FindComplexInLine($x, $y, $id)
	{
		for ($i = 0; $i < count($this->result->lines); $i++)
			for ($j = 0; $j < count($this->result->lines[$i]->slot); $j++) {
				if ($this->result->lines[$i]->slot[$j]->id == $id && $this->result->lines[$i]->slot[$j]->x == $x && $this->result->lines[$i]->slot[$j]->y == $y)
					return true;
			}
		return false;
	}
	
	function GetComplexWin($scheme, $count)
	{
		for ($i = 0; $i < count($scheme->complex); $i++)
			if ($scheme->complex[$i]->count == $count) {
				$this->lineOnly = $scheme->complex[$i]->lineOnly;
				return $scheme->complex[$i]->price;
			}
		return 0;
	}
	
	function GetLineSlot($x, $y, $id)
	{
		$lineSlot = new SlotResultLineSlot();
		$lineSlot->y = $y;
		$lineSlot->x = $x;
		$lineSlot->id = $id;
		return $lineSlot;
	}
	
	function CheckSlotLine($list, $id, $wild)
	{
		for ($i = 0; $i < count($this->counters); $i++)
			if ($this->counters[$i]->id == $id) return false;
		$isWild = in_array($id, $wild->data);
		$count_list = count($list);
		if ($count_list == 2 && !$isWild) {
			$count = 0;
			for ($i = 0; $i < $count_list; $i++)
				if (in_array($list[$i]->id, $wild->data)) $count++;
			if ($count == $count_list)
				return true;
		}
		$check = false;
		for ($i = 0; $i < $count_list; $i++)
			if ($list[$i]->id == $id) $check = true;
		return $count_list == 0 || $check || $isWild;
	}
	
	function GetPaytableList($scheme, $slot, $wild)
	{
		if (count($slot) < 2)
			return 0;
		$j = 0;
		$win = 0;
		for ($i = 0; $i < count($slot); $i++) {
			if (!in_array($slot[$i]->id, $wild->data))
				$j = $slot[$i]->id;
		}
		if ($j == 0)
			$j = $slot[0]->id;
		for ($i = 0; $i < count($scheme->slots); $i++) {
			if ($scheme->slots[$i]->id == $j) {
				$win = $this->PaytablePrice($scheme->slots[$i]->paytable, count($slot));
			}
		}
		return $win;
	}
	
	function GetPaytable($scheme, $slot, $count)
	{
		$win = 0;
		for ($i = 0; $i < count($scheme->slots); $i++) {
			if ($scheme->slots[$i]->id == $slot) {
				$win = $this->PaytablePrice($scheme->slots[$i]->paytable, $count);
			}
		}
		return $win;
	}
	
	function PaytablePrice($prices, $count)
	{
		for ($i = 0; $i < count($prices); $i++) {
			if ($prices[$i]->count == $count)
				return $prices[$i]->price;
		}
		return 0;
	}
	
	function CheckSpecials($scheme, $ignore, $getSpecial, $specialSameTime)
	{
		$checkSameTime = 0;
		$check = true;
		for ($i = 0; $i < count($this->counters); $i++) {
			$this->counters[$i]->count = 0;
			for ($y = 0; $y < $scheme->height; $y++)
				for ($x = 0; $x < $scheme->width; $x++) {
				if ($this->grid[$x][$y] == $this->counters[$i]->id)
					$this->counters[$i]->count++;
			}
			if ($this->counters[$i]->win())
			{
				$checkSameTime++;
				$this->isSpecial = true;
			}
			if ($this->CheckNameSpecial($getSpecial)) {
				if (!$this->counters[$i]->win() && $this->counters[$i]->type == $getSpecial)
					$check = false;
			}
		}
		if (!$check)
			return true;
		if ($checkSameTime > 1)
			return !$specialSameTime;
		if (empty($ignore))
			return false;
		for ($i = 0; $i < count($ignore); $i++)
			if ($this->FindSpecial($ignore[$i])) return true;
		return false;
	}
	
	function FindSpecial($type)
	{
		for ($i = 0; $i < count($this->counters); $i++) {
			if ($type == $this->counters[$i]->type && $this->counters[$i]->win())
				return true;
		}
		return false;
	}
	
	function BuildGrid($scheme, $complex, $block)
	{
		$grid = array();
		$this->result->window = array();
		$this->count = $complex ? 0 : -1;
		for ($y = 0; $y < $scheme->height; $y++) {
			$item = array();
			for ($x = 0; $x < $scheme->width; $x++) {
				$item[] = 0;
			}
			$grid[] = $item;
		}
		for ($x = 0; $x < $scheme->width; $x++) {
			$this->prev = 0;
			if ($this->count > 0)
				$this->count = -1;
			$this->list_grid = $scheme->preset;
			if ($block->isBuild()) $this->list_grid = array_diff($this->list_grid, array($block->counter->id));
			for ($y = 0; $y < $scheme->height; $y++) {
				$grid[$x][$y] = $this->list_grid[array_rand($this->list_grid)];
				if ($this->ComplexCheck($scheme, $grid[$x][$y]))
					$this->list_grid = array_diff($this->list_grid, array($grid[$x][$y]));
				$this->prev = $grid[$x][$y];
			}
		}
		for ($y = 0; $y < $scheme->height; $y++)
			for ($x = 0; $x < $scheme->width; $x++) {
				array_push($this->result->window, $grid[$x][$y]);
			}
		return $grid;
	}
	
	function ComplexCheck($scheme, $id)
	{
		if ($this->count == -1)
			return true;
		if ($this->count > 0 && $id != $this->prev) {
			$last = $this->prev;
			$this->list_grid = array_diff($this->list_grid, array($last));
			$this->count = -1;
			return true;
		}
		for ($i = 0; $i < count($scheme->slots); $i++) {
			if ($scheme->slots[$i]->id == $id && $scheme->slots[$i]->type != "Chip")
				return true;
			if ($scheme->slots[$i]->id == $id && $scheme->slots[$i]->type == "Chip" && $scheme->slots[$i]->complex) {
				$this->count += $id == $this->prev ? 1 : 0;
				$this->isComplex = $this->count > 0;
				if ($id != $this->prev)
					$this->prev = 0;
				return $id != $this->prev && $this->prev > 0;
			}
		}
		return true;
	}
	
	function CheckWild($scheme, $id)
	{
		if ($id <= 0)
			return -1;
		for ($i = 0; $i < count($scheme->slots); $i++) {
			if ($scheme->slots[$i]->id == $id && $scheme->slots[$i]->type == "Chip")
				return $id;
		}
		return -1;
	}
	
	function GetWild($scheme, $id)
	{
		$wild = new WildSlot();
		for ($i = 0; $i < count($scheme->slots); $i++) {
			if ($scheme->slots[$i]->type == "Wild")
				array_push($wild->data, $scheme->slots[$i]->id);
		}
		if ($id > 0)
			array_push($wild->data, $id);
		return $wild;
	}
	
	function GetSpecials($scheme)
	{
		$counters = array();
		for ($i = 0; $i < count($scheme->slots); $i++) {
			if ($this->CheckNameSpecial($scheme->slots[$i]->type)) {
				$special = new SpecialCounter();
				$special->type = $scheme->slots[$i]->type;
				$special->id = $scheme->slots[$i]->id;
				array_push($counters, $special);
			}
		}
		return $counters;
	}
	
	function SetLimit($scheme, $value, $bet)
	{
		if ($value <= 0)
			return $value;
		$list = array();
		for ($i = 0; $i < count($scheme->slots); $i++)
			for ($j = 0; $j < count($scheme->slots[$i]->paytable); $j++) {
			array_push($list, $scheme->slots[$i]->paytable[$j]->price);
		}
		$result = min($list) * $scheme->bets[$bet];
		return $value < $result ? 0 : $value;
	}
}
?>
