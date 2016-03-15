/*
 * Copyright 2016 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */

package monasca.common.model.metric;

import org.testng.Assert;
import org.testng.annotations.Test;

@Test
public class MetricPeriodTest {

  public void shouldReturnSparseForNegativePeriod() {
    Assert.assertTrue(MetricPeriod.isSparse(-10));
    Assert.assertFalse(MetricPeriod.isPeriodic(-10));
  }

  public void shouldReturnSparseForNegativePeriod_Metric() {
    final Metric metric = new Metric();
    metric.setPeriod(-10);

    Assert.assertTrue(MetricPeriod.isSparse(metric));
    Assert.assertFalse(MetricPeriod.isPeriodic(metric));
  }

  public void shouldReturnPeriodicForPositivePeriod() {
    Assert.assertTrue(MetricPeriod.isPeriodic(10));
    Assert.assertFalse(MetricPeriod.isSparse(10));
  }

  public void shouldReturnPeriodicForPositivePeriod_Metric() {
    final Metric metric = new Metric();
    metric.setPeriod(10);

    Assert.assertFalse(MetricPeriod.isSparse(metric));
    Assert.assertTrue(MetricPeriod.isPeriodic(metric));
  }

}
